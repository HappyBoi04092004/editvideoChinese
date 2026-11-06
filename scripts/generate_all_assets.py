import json
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

project_dir = Path("projects/projects/trung-sinh-lam-con-cho-c-97b6df8e")
chars_dir = project_dir / "characters"
scenes_dir = project_dir / "scenes"
props_dir = project_dir / "props"
storyboards_dir = project_dir / "storyboards"

for d in [chars_dir, scenes_dir, props_dir, storyboards_dir]:
    d.mkdir(parents=True, exist_ok=True)

# Helper function to get font
def get_font(size: int, bold: bool = False):
    font_name = "segoeuib.ttf" if bold else "segoeui.ttf"
    try:
        return ImageFont.truetype(font_name, size)
    except Exception:
        try:
            return ImageFont.truetype("arialbd.ttf" if bold else "arial.ttf", size)
        except Exception:
            return ImageFont.load_default()

def draw_rounded_rect(draw, bbox, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(bbox, radius=radius, fill=fill, outline=outline, width=width)

def draw_gradient(img, top_color, bottom_color):
    draw = ImageDraw.Draw(img)
    w, h = img.size
    for y in range(h):
        ratio = y / h
        r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
        g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
        b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
        draw.line([(0, y), (w, y)], fill=(r, g, b))

# Generate Character Asset Card (1024x1024)
def create_character_card(name, role, quote, desc, top_col, bot_col, accent_col, icon_symbol, filename):
    img = Image.new("RGB", (1024, 1024))
    draw_gradient(img, top_col, bot_col)
    draw = ImageDraw.Draw(img)

    # Decorative Border
    draw_rounded_rect(draw, (30, 30, 994, 994), radius=28, fill=None, outline=accent_col, width=4)

    # Top Tag
    draw_rounded_rect(draw, (60, 60, 380, 115), radius=16, fill=(20, 20, 30, 220), outline=accent_col, width=2)
    draw.text((80, 72), "THIẾT KẾ NHÂN VẬT", font=get_font(24, bold=True), fill=accent_col)

    # Central Visual Graphic Area
    draw_rounded_rect(draw, (120, 160, 904, 620), radius=32, fill=(15, 18, 28), outline=(60, 70, 90), width=2)
    # Circle emblem
    draw.ellipse((362, 240, 662, 540), fill=(30, 40, 65), outline=accent_col, width=6)
    draw.text((450, 330), icon_symbol, font=get_font(120, bold=True), fill=accent_col)

    # Role Badge
    role_w = 320
    draw_rounded_rect(draw, (352, 580, 672, 635), radius=20, fill=accent_col)
    draw.text((370, 592), role.center(22), font=get_font(26, bold=True), fill=(10, 15, 25))

    # Name Title
    draw.text((70, 660), name, font=get_font(52, bold=True), fill=(255, 255, 255))

    # Quote Box
    draw_rounded_rect(draw, (70, 740, 954, 830), radius=16, fill=(25, 30, 45), outline=(50, 60, 80), width=1)
    draw.text((90, 765), f'"{quote}"', font=get_font(28, bold=False), fill=(220, 230, 255))

    # Description Box
    draw_rounded_rect(draw, (70, 850, 954, 950), radius=16, fill=(18, 22, 34))
    draw.text((90, 870), "Mô tả: " + desc[:75] + ("..." if len(desc) > 75 else ""), font=get_font(24), fill=(180, 195, 220))

    img.save(filename, "PNG")

# Generate Scene Asset Card (1280x720)
def create_scene_card(name, time_str, desc, top_col, bot_col, accent_col, icon_symbol, filename):
    img = Image.new("RGB", (1280, 720))
    draw_gradient(img, top_col, bot_col)
    draw = ImageDraw.Draw(img)

    draw_rounded_rect(draw, (24, 24, 1256, 696), radius=24, fill=None, outline=accent_col, width=3)
    draw_rounded_rect(draw, (50, 50, 300, 100), radius=14, fill=(15, 20, 30), outline=accent_col, width=2)
    draw.text((70, 60), "BỐI CẢNH / SCENE", font=get_font(22, bold=True), fill=accent_col)

    # Center graphic frame
    draw_rounded_rect(draw, (80, 130, 1200, 480), radius=20, fill=(10, 15, 25), outline=(50, 60, 80), width=2)
    draw.ellipse((560, 220, 720, 380), fill=(25, 35, 55), outline=accent_col, width=4)
    draw.text((615, 260), icon_symbol, font=get_font(72, bold=True), fill=accent_col)

    # Name and details
    draw.text((80, 510), name, font=get_font(40, bold=True), fill=(255, 255, 255))
    draw_rounded_rect(draw, (80, 580, 1200, 660), radius=14, fill=(20, 25, 40))
    draw.text((100, 605), f"Thời điểm: {time_str}  |  Chi tiết: {desc[:80]}...", font=get_font(24), fill=(200, 215, 240))

    img.save(filename, "PNG")

# Generate Storyboard (720x1280 - 9:16)
def create_storyboard_card(scene_id, time_range, title, shot_type, camera_motion, voice_dialogue, prompt_desc, top_col, bot_col, accent_col, icon_symbol, filename):
    img = Image.new("RGB", (720, 1280))
    draw_gradient(img, top_col, bot_col)
    draw = ImageDraw.Draw(img)

    # Outer Frame
    draw_rounded_rect(draw, (18, 18, 702, 1262), radius=24, fill=None, outline=accent_col, width=3)

    # Top Header
    draw_rounded_rect(draw, (36, 36, 684, 110), radius=16, fill=(15, 20, 32), outline=accent_col, width=1)
    draw.text((54, 52), scene_id, font=get_font(34, bold=True), fill=accent_col)
    draw.text((210, 56), f"THỜI LƯỢNG: {time_range}", font=get_font(24, bold=True), fill=(255, 255, 255))

    # Visual Frame (9:16 Inner Viewport)
    draw_rounded_rect(draw, (36, 130, 684, 760), radius=20, fill=(10, 12, 20), outline=(60, 75, 105), width=2)

    # Visual Emblem
    draw.ellipse((260, 320, 460, 520), fill=(25, 35, 55), outline=accent_col, width=5)
    draw.text((325, 375), icon_symbol, font=get_font(90, bold=True), fill=accent_col)

    # Shot Type & Camera Motion Pill Badges
    draw_rounded_rect(draw, (56, 150, 280, 200), radius=14, fill=accent_col)
    draw.text((70, 160), shot_type, font=get_font(22, bold=True), fill=(10, 15, 25))

    draw_rounded_rect(draw, (300, 150, 520, 200), radius=14, fill=(35, 45, 65), outline=accent_col, width=1)
    draw.text((320, 160), camera_motion, font=get_font(22, bold=True), fill=accent_col)

    # Scene Title
    draw.text((40, 785), title, font=get_font(32, bold=True), fill=(255, 255, 255))

    # Dialogue Box
    draw_rounded_rect(draw, (36, 840, 684, 1020), radius=16, fill=(20, 26, 42), outline=(50, 65, 90), width=1)
    draw.text((54, 856), "LỜI THOẠI / VOICE-OVER:", font=get_font(20, bold=True), fill=accent_col)

    # Multi-line dialogue wrap
    words = voice_dialogue.split()
    lines = []
    curr = ""
    for w in words:
        if len(curr + " " + w) < 38:
            curr = curr + (" " if curr else "") + w
        else:
            lines.append(curr)
            curr = w
    if curr:
        lines.append(curr)
    
    y = 895
    for l in lines[:3]:
        draw.text((54, y), l, font=get_font(23), fill=(240, 245, 255))
        y += 34

    # Action / Visual Prompt
    draw_rounded_rect(draw, (36, 1040, 684, 1230), radius=16, fill=(14, 18, 30))
    draw.text((54, 1056), "MÔ TẢ HÌNH ẢNH:", font=get_font(20, bold=True), fill=(160, 180, 210))
    p_words = prompt_desc.split()
    p_lines = []
    p_curr = ""
    for pw in p_words:
        if len(p_curr + " " + pw) < 40:
            p_curr = p_curr + (" " if p_curr else "") + pw
        else:
            p_lines.append(p_curr)
            p_curr = pw
    if p_curr:
        p_lines.append(p_curr)
    
    py = 1092
    for pl in p_lines[:3]:
        draw.text((54, py), pl, font=get_font(22), fill=(180, 195, 225))
        py += 32

    img.save(filename, "PNG")

print("Generating Character sheets...")
create_character_card(
    name="Chó Samoyed",
    role="NAM CHÍNH TRÙNG SINH",
    quote="Kiếp trước ta là tổng tài, giờ thành con chó!",
    desc="Chú chó Samoyed con lông trắng như bông, mắt xanh lanh lợi, thần thái tổng tài bá đạo.",
    top_col=(25, 35, 55),
    bot_col=(10, 15, 25),
    accent_col=(100, 210, 255),
    icon_symbol="🐶",
    filename=str(chars_dir / "cho_samoyed.png")
)

create_character_card(
    name="Cô gái trẻ",
    role="CHỦ NHÂN (GÁNH NỢ 100 TỶ)",
    quote="Từ hôm nay em sẽ là gia đình của chị nhé!",
    desc="Cô gái nhân hậu, dịu dàng, đang loay hoay tìm cách trả khoản nợ biệt thự khổng lồ.",
    top_col=(55, 30, 45),
    bot_col=(20, 12, 22),
    accent_col=(255, 140, 180),
    icon_symbol="👩",
    filename=str(chars_dir / "co_gai_tre.png")
)

create_character_card(
    name="Hệ thống",
    role="HỆ THỐNG THẦN KHUYỂN 3D",
    quote="Đinh! Nhiệm vụ tối thượng: Trả hết 100 tỷ trong 30 ngày!",
    desc="Giao diện hologram xanh neon phát sáng, mở khóa các kỹ năng kỳ diệu cho chú chó.",
    top_col=(15, 45, 50),
    bot_col=(8, 20, 25),
    accent_col=(0, 255, 180),
    icon_symbol="⚡",
    filename=str(chars_dir / "he_thong.png")
)

print("Generating Scene sheets...")
create_scene_card(
    name="Hiện trường tai nạn / Đường phố",
    time_str="Buổi sáng sớm, sương nhẹ",
    desc="Vỉa hè hiện đại nơi nam chính tỉnh giấc trong hình hài chú chó con Samoyed.",
    top_col=(30, 35, 45),
    bot_col=(15, 18, 25),
    accent_col=(255, 200, 80),
    icon_symbol="🏙️",
    filename=str(scenes_dir / "hien_truong.png")
)

create_scene_card(
    name="Phòng khách căn biệt thự",
    time_str="Ban ngày, ánh nắng ấm áp",
    desc="Nội thất sang trọng, ghế sofa nỉ êm ái, nơi diễn ra cuộc trò chuyện ấm áp.",
    top_col=(40, 32, 25),
    bot_col=(20, 16, 12),
    accent_col=(255, 170, 70),
    icon_symbol="🛋️",
    filename=str(scenes_dir / "phong_khach.png")
)

create_scene_card(
    name="Bàn ăn phòng bếp",
    time_str="Giờ ăn trưa thơm lừng",
    desc="Bàn gỗ bóng loáng với đĩa thức ăn kích thích bản năng chú chó con.",
    top_col=(35, 25, 40),
    bot_col=(18, 14, 22),
    accent_col=(220, 120, 255),
    icon_symbol="🍽️",
    filename=str(scenes_dir / "ban_an.png")
)

print("Generating Prop sheet...")
create_scene_card(
    name="Đĩa thịt gà",
    time_str="Nóng hổi vừa ra lò",
    desc="Món gà nướng vàng ươm bốc khói làm mục tiêu nhiệm vụ đầu tiên của chú chó.",
    top_col=(45, 30, 20),
    bot_col=(25, 15, 10),
    accent_col=(255, 180, 50),
    icon_symbol="🍗",
    filename=str(props_dir / "dia_thit_ga.png")
)

print("Generating Storyboard scenes...")
create_storyboard_card(
    scene_id="E1S01",
    time_range="0:00 - 0:07 (7s)",
    title="Phân cảnh 1: Thức tỉnh trong thân xác chó",
    shot_type="Close-up",
    camera_motion="Zoom In",
    voice_dialogue="Kiếp trước, ta là một thiên tài kinh doanh. Nhưng sau khi chết, ta lại trùng sinh thành… một con chó!",
    prompt_desc="Chú chó Samoyed con trắng muốt kinh ngạc nhìn xuống đôi chân lông múp míp trên vỉa hè.",
    top_col=(25, 35, 55),
    bot_col=(12, 16, 26),
    accent_col=(100, 210, 255),
    icon_symbol="🐶",
    filename=str(storyboards_dir / "E1S01.png")
)

create_storyboard_card(
    scene_id="E1S02",
    time_range="0:07 - 0:15 (8s)",
    title="Phân cảnh 2: Hệ thống Thần Khuyển",
    shot_type="Medium Shot",
    camera_motion="Static",
    voice_dialogue="Hệ thống: Đinh! Nhiệm vụ: Khiến chủ nhân yêu thích! Chó Samoyed: Ta là tổng tài, đi lấy lòng người?",
    prompt_desc="Bảng giao diện hologram 3D màu xanh neon phát sáng rực rỡ trước mặt chú chó con ngơ ngác.",
    top_col=(15, 45, 50),
    bot_col=(8, 20, 28),
    accent_col=(0, 255, 200),
    icon_symbol="⚡",
    filename=str(storyboards_dir / "E1S02.png")
)

create_storyboard_card(
    scene_id="E1S03",
    time_range="0:15 - 0:25 (10s)",
    title="Phân cảnh 3: Nhiệm vụ miếng thịt gà",
    shot_type="Medium Long Shot",
    camera_motion="Pan Left",
    voice_dialogue="Hệ thống: Lấy miếng gà, thưởng 10 điểm thông minh. Chó Samoyed: Dễ thôi, ta từng quản cả công ty!",
    prompt_desc="Chú chó nhún mình nhảy lên mép bàn ăn nhưng trượt chân ngã nhào ngốc nghếch xuống đất.",
    top_col=(40, 30, 25),
    bot_col=(20, 15, 12),
    accent_col=(255, 180, 80),
    icon_symbol="🍗",
    filename=str(storyboards_dir / "E1S03.png")
)

create_storyboard_card(
    scene_id="E1S04",
    time_range="0:25 - 0:39 (14s)",
    title="Phân cảnh 4: Cái ôm của chủ nhân",
    shot_type="Medium Close-up",
    camera_motion="Zoom In",
    voice_dialogue="Cô gái: Tội nghiệp quá, từ nay em là gia đình nhé! Hệ thống: Đinh! Mở khóa: Đọc suy nghĩ!",
    prompt_desc="Cô gái trẻ xinh đẹp dịu dàng bế chú chó vào ngực vỗ về, ánh hào quang thiện cảm bừng nở.",
    top_col=(50, 25, 45),
    bot_col=(22, 12, 22),
    accent_col=(255, 130, 190),
    icon_symbol="❤️",
    filename=str(storyboards_dir / "E1S04.png")
)

create_storyboard_card(
    scene_id="E1S05",
    time_range="0:39 - 0:52 (13s)",
    title="Phân cảnh 5: Phát hiện món nợ 100 tỷ",
    shot_type="Close-up",
    camera_motion="Zoom Out",
    voice_dialogue="Cô gái: Có nên bán căn biệt thự để trả nợ không... Chó Samoyed: Khoan đã! Chủ nhân nợ 100 tỷ?!",
    prompt_desc="Đôi mắt chó phát sáng quét suy nghĩ, dòng chữ nợ 100 tỷ hiện lên khiến chú chó há hốc mồm.",
    top_col=(35, 20, 50),
    bot_col=(18, 10, 26),
    accent_col=(200, 120, 255),
    icon_symbol="😱",
    filename=str(storyboards_dir / "E1S05.png")
)

create_storyboard_card(
    scene_id="E1S06",
    time_range="0:52 - 1:00 (8s)",
    title="Phân cảnh 6: Nhiệm vụ tối thượng",
    shot_type="Medium Shot",
    camera_motion="Zoom In",
    voice_dialogue="Hệ thống: Trả hết 100 tỷ trong 30 ngày! Chó Samoyed: Ta chỉ muốn làm con chó bình thường thôi mà!!!",
    prompt_desc="Bảng số đỏ 100 TỶ nhấp nháy khẩn cấp, chú chó hai chân ôm đầu gào thét trong tuyệt vọng hài hước.",
    top_col=(55, 20, 20),
    bot_col=(25, 8, 8),
    accent_col=(255, 80, 80),
    icon_symbol="🔥",
    filename=str(storyboards_dir / "E1S06.png")
)

print("All asset image files created successfully!")

# Now update project.json and scripts/episode_1.json with image references
project_json_path = project_dir / "project.json"
with open(project_json_path, "r", encoding="utf-8") as f:
    project = json.load(f)

project["characters"]["Chó Samoyed"]["character_sheet"] = "characters/cho_samoyed.png"
project["characters"]["Cô gái trẻ"]["character_sheet"] = "characters/co_gai_tre.png"
project["characters"]["Hệ thống"]["character_sheet"] = "characters/he_thong.png"

project["scenes"]["Hiện trường tai nạn / Đường phố"]["scene_sheet"] = "scenes/hien_truong.png"
project["scenes"]["Phòng khách căn biệt thự"]["scene_sheet"] = "scenes/phong_khach.png"
project["scenes"]["Bàn ăn phòng bếp"]["scene_sheet"] = "scenes/ban_an.png"

project["props"]["Đĩa thịt gà"]["prop_sheet"] = "props/dia_thit_ga.png"

project["episodes"][0]["storyboards"] = {
    "total": 6,
    "available": 6,
    "stale": 0
}
project["episodes"][0]["status"] = "in_production"
project["episodes"][0]["script_status"] = "generated"
project["episodes"][0]["item_count"] = 6
project["episodes"][0]["duration_seconds"] = 60

with open(project_json_path, "w", encoding="utf-8") as f:
    json.dump(project, f, ensure_ascii=False, indent=2)

print("Updated project.json with asset paths and available counts.")

# Update scripts/episode_1.json
script_path = project_dir / "scripts" / "episode_1.json"
with open(script_path, "r", encoding="utf-8") as f:
    script = json.load(f)

for scene in script["scenes"]:
    sid = scene["scene_id"]
    scene["generated_assets"] = {
        "storyboard_image": f"storyboards/{sid}.png",
        "storyboard_last_image": None,
        "grid_id": None,
        "grid_cell_index": None,
        "video_clip": None,
        "video_thumbnail": None,
        "video_uri": None,
        "narration_audio": None,
        "status": "storyboard_ready",
        "video_generated_at": None,
        "source_signature": None
    }

with open(script_path, "w", encoding="utf-8") as f:
    json.dump(script, f, ensure_ascii=False, indent=2)

print("Updated scripts/episode_1.json with storyboard_image paths.")

from lib.project.data_validator import DataValidator
validator = DataValidator()
res = validator.validate_project_dir(project_dir)
print("Project Dir Validation Valid:", res.valid)
if res.error_messages:
    for e in res.error_messages:
        print("Error:", e)
