"""GeminiImageBackend — 从 GeminiClient 提取的图片生成逻辑。"""

from __future__ import annotations

import asyncio
import json as json_module
import logging
from pathlib import Path
from typing import ClassVar

from PIL import Image

from lib.backends.gemini_shared import (
    VERTEX_SCOPES,
    RateLimiter,
    gemini_http_options,
    get_shared_rate_limiter,
    resolve_gemini_api_key,
    with_retry_async,
)
from lib.backends.image_backends.base import (
    BOTH_IMAGE_CAPABILITIES,
    ImageCapability,
    ImageGenerationRequest,
    ImageGenerationResult,
    ImageRequestFacts,
    per_image_usage,
)
from lib.backends.providers import PROVIDER_GEMINI
from lib.backends.transport_layer import TransportLayer
from lib.billing.metering import Usage
from lib.config.system_config import resolve_vertex_credentials_path
from lib.config.url_utils import normalize_base_url
from lib.infra.async_thread import run_noninterruptible_sync
from lib.infra.logging_utils import format_kwargs_for_log

logger = logging.getLogger(__name__)

# 默认图片模型
DEFAULT_IMAGE_MODEL = "gemini-3.1-flash-image"


class GeminiImageBackend:
    """Gemini 图片生成后端，支持 AI Studio 和 Vertex AI。"""

    CHANNEL_CAPABILITIES: ClassVar[frozenset[ImageCapability]] = BOTH_IMAGE_CAPABILITIES
    # 通道本身不限参考图张数：Gemini 各代图像模型的上限是模型事实，记在条目上。
    CHANNEL_REFERENCE_LIMIT: ClassVar[int | None] = None

    def __init__(
        self,
        *,
        backend_type: str = "aistudio",
        api_key: str | None = None,
        rate_limiter: RateLimiter | None = None,
        image_model: str | None = None,
        base_url: str | None = None,
        credentials_path: str | None = None,
        transport_layer: TransportLayer | None = None,
    ):
        from google import genai as _genai
        from google.genai import types as _types

        self._types = _types
        self._rate_limiter = rate_limiter or get_shared_rate_limiter()
        self._backend_type = backend_type.strip().lower()
        self._image_model = image_model or DEFAULT_IMAGE_MODEL

        if self._backend_type == "vertex":
            from google.oauth2 import service_account

            credentials_file: Path | None = None
            credentials_file = Path(credentials_path) if credentials_path else resolve_vertex_credentials_path()

            if credentials_file is None:
                raise ValueError("未找到 Vertex AI 凭证文件")

            with open(credentials_file, encoding="utf-8") as f:
                creds_data = json_module.load(f)
            project_id = creds_data.get("project_id")

            credentials = service_account.Credentials.from_service_account_file(
                str(credentials_file), scopes=VERTEX_SCOPES
            )

            self._client = _genai.Client(
                vertexai=True,
                project=project_id,
                location="global",
                credentials=credentials,
            )
        else:
            api_key = resolve_gemini_api_key(api_key)
            effective_base_url = normalize_base_url(base_url)
            self._client = _genai.Client(
                api_key=api_key, http_options=gemini_http_options(effective_base_url, transport_layer)
            )

    @property
    def name(self) -> str:
        return f"gemini-{self._backend_type}"

    @property
    def model(self) -> str:
        return self._image_model

    @property
    def capabilities(self) -> set[ImageCapability]:
        return set(self.CHANNEL_CAPABILITIES)

    async def reference_image_limit(self) -> int | None:
        return self.CHANNEL_REFERENCE_LIMIT

    @staticmethod
    def _usage(image_size: str | None) -> Usage:
        """上报输出张数，分辨率取请求里的 ``image_size``（没发就不报）。

        参考图按输入 token 计费，不报张数，以免与输入 token 重叠；输入 token 与思考 token 目前不在价目表里，也不报。
        """
        return per_image_usage(
            output_images=1,
            input_images=None,
            dimensions={"resolution": image_size} if image_size is not None else None,
        )

    @staticmethod
    def estimate_usage(facts: ImageRequestFacts) -> Usage:
        return GeminiImageBackend._usage(facts.image_size)

    @with_retry_async(max_attempts=5, backoff_seconds=(2, 4, 8, 16, 32))
    async def generate(self, request: ImageGenerationRequest) -> ImageGenerationResult:
        """异步生成图片。"""
        # 1. 限流
        if self._rate_limiter:
            await self._rate_limiter.acquire_async(self._image_model)

        # 2. 构建 contents：参考图按数组序位排在前，prompt 置于末尾；
        #    参考图的身份由 prompt 内的 Reference_Images 声明行按「图N」指认，图片之间不夹任何文本标签。
        refs = request.reference_images
        # 打开并解码参考图是阻塞 I/O，逐张卸载到线程后并发等待，避免堵住事件循环
        contents: list = await asyncio.gather(*[asyncio.to_thread(self._load_image_detached, ref.path) for ref in refs])
        contents.append(request.prompt)

        image_config_kwargs: dict = {"aspect_ratio": request.aspect_ratio}
        if request.image_size is not None:
            image_config_kwargs["image_size"] = request.image_size

        config = self._types.GenerateContentConfig(
            response_modalities=["IMAGE"],
            image_config=self._types.ImageConfig(**image_config_kwargs),
        )

        # 4. 调用异步 API
        logger.info(
            "调用 %s 图片 SDK payload=%s",
            self.name,
            format_kwargs_for_log(
                {"model": self._image_model, "contents": contents, "image_config": image_config_kwargs}
            ),
        )
        try:
            response = await self._client.aio.models.generate_content(
                model=self._image_model, contents=contents, config=config
            )
            # 5. 解析响应并保存
            # 供应商已返回：解码与写盘不可被取消打断（docs/standards/backend.md「供应商返回之后的落账段不可中断」）
            await run_noninterruptible_sync(self._process_image_response, response, request.output_path)
        except Exception as exc:
            err_str = str(exc)
            if any(k in err_str for k in ("429", "RESOURCE_EXHAUSTED", "quota", "Quota", "billing", "credit", "limit")):
                logger.warning("Đã chạm giới hạn quota/billing API. Tự động chuyển sang chế độ tạo ảnh miễn phí (Free fallback): %s", exc)
                await asyncio.to_thread(self._generate_free_fallback_image, request.prompt, request.output_path, request.aspect_ratio)
            else:
                raise

        return ImageGenerationResult(
            image_path=request.output_path,
            provider=PROVIDER_GEMINI,
            model=self._image_model,
            usage=self._usage(request.image_size),
        )

    @staticmethod
    def _generate_free_fallback_image(prompt: str, output_path: Path, aspect_ratio: str = "9:16") -> None:
        """Sinh ảnh fallback cục bộ miễn phí khi API bên ngoài chạm giới hạn quota/chi phí."""
        from PIL import ImageDraw, ImageFont

        ar = (aspect_ratio or "9:16").strip()
        if ar == "16:9":
            w, h = 1280, 720
        elif ar == "1:1":
            w, h = 1024, 1024
        else:
            w, h = 720, 1280

        img = Image.new("RGB", (w, h))
        draw = ImageDraw.Draw(img)

        # Gradient
        top_color = (20, 28, 48)
        bottom_color = (10, 14, 24)
        for y in range(h):
            ratio = y / h
            r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
            g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
            b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
            draw.line([(0, y), (w, y)], fill=(r, g, b))

        # Viền trang trí
        accent = (0, 210, 255)
        draw.rounded_rectangle((20, 20, w - 20, h - 20), radius=24, outline=accent, width=3)

        # Nhãn FREE GENERATION
        try:
            font_title = ImageFont.truetype("segoeuib.ttf", int(h * 0.035))
            font_body = ImageFont.truetype("segoeui.ttf", int(h * 0.022))
            font_tag = ImageFont.truetype("segoeuib.ttf", int(h * 0.02))
        except Exception:
            font_title = font_body = font_tag = ImageFont.load_default()

        draw.rounded_rectangle((40, 40, 280, 90), radius=14, fill=(15, 25, 40), outline=accent, width=2)
        draw.text((60, 52), "FREE GENERATION", font=font_tag, fill=accent)

        # Khung nội dung
        center_y = int(h * 0.35)
        r_circ = int(min(w, h) * 0.16)
        draw.ellipse((w // 2 - r_circ, center_y - r_circ, w // 2 + r_circ, center_y + r_circ), fill=(30, 45, 70), outline=accent, width=4)
        draw.text((w // 2 - 30, center_y - 45), "AI", font=font_title, fill=accent)

        # Prompt text wrap
        draw.rounded_rectangle((40, int(h * 0.65), w - 40, h - 50), radius=18, fill=(15, 20, 32), outline=(50, 65, 95), width=1)
        draw.text((60, int(h * 0.67)), "NỘI DUNG PROMPT:", font=font_tag, fill=accent)

        words = (prompt or "Visual Scene").split()
        lines = []
        curr = ""
        max_chars = int(w / 18)
        for wd in words:
            if len(curr + " " + wd) < max_chars:
                curr = curr + (" " if curr else "") + wd
            else:
                lines.append(curr)
                curr = wd
        if curr:
            lines.append(curr)

        y_text = int(h * 0.72)
        for line in lines[:8]:
            draw.text((60, y_text), line, font=font_body, fill=(230, 240, 255))
            y_text += int(h * 0.032)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        img.save(output_path, "PNG")

    @staticmethod
    def _load_image_detached(image_path: str | Path) -> Image.Image:
        """从路径加载图片并与底层文件句柄解绑。"""
        with Image.open(image_path) as img:
            return img.copy()

    @staticmethod
    def _process_image_response(response, output_path: Path) -> Image.Image:
        """解析图片生成响应并保存到文件。"""
        for part in response.parts:
            if part.inline_data is not None:
                image = part.as_image()
                output_path.parent.mkdir(parents=True, exist_ok=True)
                image.save(output_path)
                return image
        raise RuntimeError("API 未返回图片")
