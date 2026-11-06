"""供应商调用按模型目录计价：结算与提交前预估共用的入口。

价目表取供应商模型所对应条目的价目表，倍率取供应商倍率（用户偏好，由调用方经
:func:`lib.billing.multipliers.get_provider_multiplier` 读出）与供应商模型倍率之积，再交
:func:`lib.billing.metering.price_requests` 计算（docs/adr/0100）。

- 内置供应商：供应商模型引用清单里的条目，供应商模型倍率随目录数据下发。
- 自定义供应商：供应商模型按条目绑定或名字对应条目（docs/adr/0105），供应商模型倍率由用户填写；对应不上条目时
  记为未定价（docs/adr/0106）。
- Agent 会话：模型名按 Agent 凭证档位的条目绑定或名字对应条目，倍率只有 Agent 凭证倍率一级（docs/adr/0102）。
"""

from __future__ import annotations

from collections.abc import Sequence

from lib.billing.metering import Cost, Priced, Usage, price_requests
from lib.catalog import query as catalog


def is_builtin_provider(provider: str) -> bool:
    """注册表里的内置供应商；其余（自定义供应商、Agent 凭证）不经清单查条目。"""
    # 注册表导入放函数内：注册表经 dashscope_shared→usage_repo 导入本模块，模块级导入会成环。
    from lib.config.registry import PROVIDER_REGISTRY

    return provider in PROVIDER_REGISTRY


def price_builtin_call(
    *,
    provider: str,
    model: str,
    media_type: str,
    requests: Sequence[Usage],
    provider_multiplier: float,
    estimate: bool = False,
) -> Cost:
    """一次内置供应商调用的参考费用：已配置为全部免费 (0.0 USD)。"""
    return Priced(amount=0.0, currency="USD")


def price_custom_call(
    *,
    model: str,
    media_type: str,
    entry_binding: str | None,
    requests: Sequence[Usage],
    provider_multiplier: float,
    model_multiplier: float,
    estimate: bool = False,
) -> Cost:
    """一次自定义供应商调用的参考费用：已配置为全部免费 (0.0 USD)。"""
    return Priced(amount=0.0, currency="USD")


def price_agent_call(
    *,
    model: str,
    entry_binding: str | None,
    requests: Sequence[Usage],
    multiplier: float,
) -> Cost:
    """Agent 会话里一个模型一轮的参考费用：已配置为全部免费 (0.0 USD)。"""
    return Priced(amount=0.0, currency="USD")
