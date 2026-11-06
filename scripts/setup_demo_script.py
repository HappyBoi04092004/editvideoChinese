import json
from pathlib import Path
from lib.project.data_validator import DataValidator
from lib.script.script_models import DramaEpisodeScript

project_dir = Path("projects/projects/trung-sinh-lam-con-cho-c-97b6df8e")
project_json_path = project_dir / "project.json"
scripts_dir = project_dir / "scripts"
scripts_dir.mkdir(parents=True, exist_ok=True)

# 1. Prepare Episode 1 Drama Script
episode_1_data = {
    "title": "Tập 1: Thần Khuyển Thức Tỉnh",
    "content_mode": "drama",
    "novel": {
        "title": "Trùng sinh làm con chó có hệ thống",
        "chapter": "Tập 1"
    },
    "scenes": [
        {
            "scene_id": "E1S01",
            "duration_seconds": 7,
            "segment_break": False,
            "characters_in_scene": ["Chó Samoyed"],
            "scenes": ["Hiện trường tai nạn / Đường phố"],
            "props": [],
            "utterances": [
                {
                    "kind": "voiceover",
                    "speaker": None,
                    "text": "Kiếp trước, ta là một thiên tài kinh doanh. Nhưng sau khi chết, ta lại trùng sinh thành… một con chó!"
                }
            ],
            "source_text": "PHÂN CẢNH 1 — 0:00–0:07 | HOOK Hình ảnh: Nam chính gặp tai nạn. Màn hình tối đen, sau đó mở mắt trong thân xác một chú chó con.",
            "scene_description": "Nam chính gặp tai nạn, mở mắt ra thấy mình trong thân xác một chú chó con Samoyed trắng muốt, bàng hoàng nhận ra sự thật.",
            "image_prompt": {
                "scene": "Một chú chó Samoyed con lông trắng như tuyết, đôi mắt xanh biếc mở to kinh ngạc nhìn xuống đôi chân lông múp míp của mình trên vỉa hè góc phố thành phố.",
                "composition": {
                    "shot_type": "Close-up",
                    "lighting": "Ánh sáng ban ngày điện ảnh, ánh nắng dịu nhẹ rọi lên bộ lông trắng mềm mại",
                    "ambiance": "Ngỡ ngàng, hài hước, phong cách 3D Anime Cinematic sống động"
                }
            },
            "video_prompt": {
                "action": "Chú chó Samoyed con chớp mắt bối rối, ngơ ngác giơ hai chân trước lên ngắm nghía rồi kinh hãi lắc đầu hoảng loạn.",
                "camera_motion": "Zoom In",
                "ambiance_audio": "Âm thanh đường phố xe cộ mờ ảo, tiếng tim đập hồi hộp và tiếng thở gấp ngạc nhiên"
            }
        },
        {
            "scene_id": "E1S02",
            "duration_seconds": 8,
            "segment_break": True,
            "characters_in_scene": ["Chó Samoyed", "Hệ thống"],
            "scenes": ["Phòng khách căn biệt thự"],
            "props": [],
            "utterances": [
                {
                    "kind": "dialogue",
                    "speaker": "Hệ thống",
                    "text": "Đinh! Hệ thống Thần Khuyển đã kích hoạt. Nhiệm vụ đầu tiên: Khiến chủ nhân yêu thích ngươi."
                },
                {
                    "kind": "dialogue",
                    "speaker": "Chó Samoyed",
                    "text": "Cái gì? Ta đường đường là tổng tài, giờ phải đi lấy lòng con người?"
                }
            ],
            "source_text": "PHÂN CẢNH 2 — 0:07–0:15 | HỆ THỐNG XUẤT HIỆN Hình ảnh: Một bảng giao diện màu xanh phát sáng xuất hiện trước mắt chú chó.",
            "scene_description": "Bảng giao diện hệ thống hologram màu xanh neon phát sáng xuất hiện trước mắt chú chó Samoyed con, giao nhiệm vụ đầu tiên.",
            "image_prompt": {
                "scene": "Trước mặt chú chó Samoyed con là một màn hình giao diện công nghệ hologram 3D bán trong suốt màu xanh neon rực rỡ trong phòng khách sang trọng.",
                "composition": {
                    "shot_type": "Medium Shot",
                    "lighting": "Ánh sáng xanh neon viễn tưởng phản chiếu lung linh trong đôi mắt xanh của chú chó",
                    "ambiance": "Khoa học viễn tưởng kết hợp hài hước, rực rỡ và thần kỳ"
                }
            },
            "video_prompt": {
                "action": "Bảng hệ thống màu xanh phát sáng rung rinh trong không trung, chú chó Samoyed ngửa cổ nhìn trừng trừng với vẻ mặt cạn lời.",
                "camera_motion": "Static",
                "ambiance_audio": "Tiếng chuông hệ thống 'Đinh!' vui nhộn, âm thanh vi tính công nghệ cao"
            }
        },
        {
            "scene_id": "E1S03",
            "duration_seconds": 10,
            "segment_break": False,
            "characters_in_scene": ["Chó Samoyed", "Hệ thống"],
            "scenes": ["Bàn ăn phòng bếp"],
            "props": ["Đĩa thịt gà"],
            "utterances": [
                {
                    "kind": "dialogue",
                    "speaker": "Hệ thống",
                    "text": "Nhiệm vụ: Lấy được miếng thịt gà. Phần thưởng: cộng 10 điểm thông minh."
                },
                {
                    "kind": "dialogue",
                    "speaker": "Chó Samoyed",
                    "text": "Dễ thôi! Ta từng điều hành cả công ty!"
                }
            ],
            "source_text": "PHÂN CẢNH 3 — 0:15–0:25 | NHIỆM VỤ ĐẦU TIÊN Hình ảnh: Chó con nhìn thấy miếng thịt gà trên bàn, quyết tâm nhảy lên lấy.",
            "scene_description": "Chú chó Samoyed nhìn đĩa thịt gà trên bàn ăn cao, hùng dũng nhảy lên nhưng trượt chân ngã nhào ngốc nghếch.",
            "image_prompt": {
                "scene": "Trên bàn ăn gỗ bóng loáng có đĩa thịt gà nướng vàng ươm thơm phức, phía dưới chân bàn chú chó Samoyed nhỏ nhắn đang ngước nhìn đầy quyết tâm.",
                "composition": {
                    "shot_type": "Medium Long Shot",
                    "lighting": "Ánh đèn chùm phòng bếp ấm cúng chiếu rọi đĩa thức ăn hấp dẫn",
                    "ambiance": "Vui nhộn, đáng yêu, chuẩn bị cho cú ngã hài hước"
                }
            },
            "video_prompt": {
                "action": "Chú chó con nhún mình nhảy phốc lên mép bàn nhưng hai chân trước trượt móng vuốt, ngã lăn quay một vòng xuống tấm thảm mềm.",
                "camera_motion": "Pan Left",
                "ambiance_audio": "Tiếng nhảy phịch, tiếng trượt ngã vui tai và tiếng kêu 'ẳng' nhỏ nhẹ dễ thương"
            }
        },
        {
            "scene_id": "E1S04",
            "duration_seconds": 14,
            "segment_break": True,
            "characters_in_scene": ["Chó Samoyed", "Cô gái trẻ", "Hệ thống"],
            "scenes": ["Phòng khách căn biệt thự"],
            "props": [],
            "utterances": [
                {
                    "kind": "dialogue",
                    "speaker": "Cô gái trẻ",
                    "text": "Tội nghiệp quá! Từ hôm nay em sẽ là gia đình của chị nhé!"
                },
                {
                    "kind": "dialogue",
                    "speaker": "Hệ thống",
                    "text": "Đinh! Độ thiện cảm của chủ nhân đạt 100%. Mở khóa kỹ năng: Đọc suy nghĩ!"
                }
            ],
            "source_text": "PHÂN CẢNH 4 — 0:25–0:39 | PLOT TWIST Hình ảnh: Cô gái trẻ nhặt chú chó lên và ôm vào lòng.",
            "scene_description": "Cô gái trẻ nhân hậu cúi xuống bế chú chó con vào lòng vỗ về âu yếm, mở khóa thành tựu và kỹ năng mới từ hệ thống.",
            "image_prompt": {
                "scene": "Một cô gái trẻ xinh xắn, mái tóc buông lỏng tự nhiên, nụ cười dịu dàng ôm chú chó Samoyed trắng muốt vào lòng đầy yêu thương.",
                "composition": {
                    "shot_type": "Medium Close-up",
                    "lighting": "Ánh sáng ấm áp chan hòa tạo cảm giác an toàn, hạnh phúc",
                    "ambiance": "Cảm động, ngọt ngào, ấm áp tình gia đình"
                }
            },
            "video_prompt": {
                "action": "Cô gái trẻ ôm chú chó vào ngực xoa đầu, chú chó ngơ ngác rồi màn hình hệ thống bùng nổ hiệu ứng pháo hoa mở khóa kỹ năng.",
                "camera_motion": "Zoom In",
                "ambiance_audio": "Âm thanh xoa lông êm dịu, tiếng nhạc mở khóa kỹ năng thần thánh vang lên rộn rã"
            }
        },
        {
            "scene_id": "E1S05",
            "duration_seconds": 13,
            "segment_break": False,
            "characters_in_scene": ["Chó Samoyed", "Cô gái trẻ"],
            "scenes": ["Phòng khách căn biệt thự"],
            "props": [],
            "utterances": [
                {
                    "kind": "dialogue",
                    "speaker": "Cô gái trẻ",
                    "text": "Không biết ngày mai có nên bán căn biệt thự này để trả nợ không…"
                },
                {
                    "kind": "dialogue",
                    "speaker": "Chó Samoyed",
                    "text": "Khoan đã! Chủ nhân của ta đang nợ 100 tỷ?!"
                }
            ],
            "source_text": "PHÂN CẢNH 5 — 0:39–0:52 | BÍ MẬT Hình ảnh: Đôi mắt chó con phát sáng. Những dòng suy nghĩ của cô gái hiện lên.",
            "scene_description": "Kỹ năng đọc suy nghĩ kích hoạt, chú chó Samoyed phát hiện bí mật chấn động: chủ nhân xinh đẹp đang gánh khoản nợ khổng lồ 100 tỷ.",
            "image_prompt": {
                "scene": "Góc nhìn cận cảnh đôi mắt xanh của chú chó Samoyed phát sáng ánh kim rực rỡ, phản chiếu hình ảnh cô gái ngồi trầm tư buồn rầu cùng dòng suy nghĩ trôi nổi.",
                "composition": {
                    "shot_type": "Close-up",
                    "lighting": "Tương phản ánh sáng kịch tính, bóng tối đổ dài trên gương mặt lo lắng của cô gái",
                    "ambiance": "Căng thẳng, hồi hộp, cú ngoặt kịch tính của cốt truyện"
                }
            },
            "video_prompt": {
                "action": "Cô gái thở dài nhìn xa xăm, mắt chú chó mở to hết cỡ vì sốc, miệng há hốc kinh hoàng.",
                "camera_motion": "Zoom Out",
                "ambiance_audio": "Tiếng thở dài u sầu của cô gái, âm thanh chấn động giật thót 'Dun dun dun!'"
            }
        },
        {
            "scene_id": "E1S06",
            "duration_seconds": 8,
            "segment_break": False,
            "characters_in_scene": ["Chó Samoyed", "Hệ thống"],
            "scenes": ["Phòng khách căn biệt thự"],
            "props": [],
            "utterances": [
                {
                    "kind": "dialogue",
                    "speaker": "Hệ thống",
                    "text": "Nhiệm vụ tối thượng: Giúp chủ nhân trả hết 100 tỷ trong 30 ngày."
                },
                {
                    "kind": "dialogue",
                    "speaker": "Chó Samoyed",
                    "text": "Ta chỉ muốn làm một con chó bình thường thôi mà!!!"
                }
            ],
            "source_text": "PHÂN CẢNH 6 — 0:52–1:00 | CLIFFHANGER Hình ảnh: Giao diện hệ thống hiện nhiệm vụ mới, chó con đứng hình vì sốc.",
            "scene_description": "Hệ thống giao nhiệm vụ tối thượng bất khả thi, chú chó Samoyed ôm đầu gào thét trong tuyệt vọng tạo đoạn kết lôi cuốn.",
            "image_prompt": {
                "scene": "Bảng hệ thống màu đỏ cảnh báo hiện chữ số nợ 100 TỶ NHIỆM VỤ TỐI THƯỢNG, chú chó Samoyed hai chân ôm chặt đầu biểu cảm tuyệt vọng hài hước.",
                "composition": {
                    "shot_type": "Medium Shot",
                    "lighting": "Ánh sáng đỏ cảnh báo pha trộn ánh sáng hài hước châm biếm",
                    "ambiance": "Cười ra nước mắt, kết thúc tập 1 với cảm giác gay cấn tột đỉnh"
                }
            },
            "video_prompt": {
                "action": "Chữ 100 TỶ nhấp nháy đỏ rực, chú chó ngã ngửa ra sau bất tỉnh nhân sự, dòng chữ 'Liệu chú chó có thể cứu gia đình?' hiện lên.",
                "camera_motion": "Zoom In",
                "ambiance_audio": "Tiếng còi báo động khẩn cấp 'Wop wop', tiếng kêu gào hài hước và tiếng nhạc kết phim"
            }
        }
    ]
}

# Validate with Pydantic model
validated_script = DramaEpisodeScript.model_validate(episode_1_data)
episode_1_file = scripts_dir / "episode_1.json"
with open(episode_1_file, "w", encoding="utf-8") as f:
    json.dump(validated_script.model_dump(), f, ensure_ascii=False, indent=2)

print("Saved scripts/episode_1.json successfully.")

# 2. Update project.json
with open(project_json_path, "r", encoding="utf-8") as f:
    project = json.load(f)

project["characters"] = {
    "Chó Samoyed": {
        "description": "Chú chó Samoyed con lông trắng muốt như tuyết, mắt xanh tròn xoe, biểu cảm cực kỳ hài hước. Kiếp trước là tổng tài thiên tài kinh doanh trùng sinh.",
        "character_sheet": None,
        "reference_image": None,
        "reference_audio": None
    },
    "Cô gái trẻ": {
        "description": "Cô gái trẻ nhân hậu, xinh đẹp, mái tóc dài buộc gọn tự nhiên. Chủ nhân mới của chú chó, đang gánh món nợ bất ngờ 100 tỷ.",
        "character_sheet": None,
        "reference_image": None,
        "reference_audio": None
    },
    "Hệ thống": {
        "description": "Giao diện hệ thống Thần Khuyển dạng hologram 3D màu xanh neon phát sáng lơ lửng, thường xuyên giao các nhiệm vụ dở khóc dở cười.",
        "character_sheet": None,
        "reference_image": None,
        "reference_audio": None
    }
}

project["scenes"] = {
    "Hiện trường tai nạn / Đường phố": {
        "description": "Vỉa hè góc phố thành phố hiện đại, dòng xe cộ qua lại mờ ảo trong ánh nắng sớm.",
        "scene_sheet": None
    },
    "Phòng khách căn biệt thự": {
        "description": "Phòng khách căn biệt thự ấm cúng với sofa bọc nỉ cao cấp, thảm trải sàn mềm mại và ánh đèn vàng dịu nhẹ.",
        "scene_sheet": None
    },
    "Bàn ăn phòng bếp": {
        "description": "Khu vực bàn ăn gỗ bóng loáng trong phòng bếp ấm cúng, trên bàn có đĩa thịt gà thơm lừng.",
        "scene_sheet": None
    }
}

project["props"] = {
    "Đĩa thịt gà": {
        "description": "Đĩa sứ trắng đựng miếng thịt gà nướng vàng ươm bốc khói nghi ngút thơm lừng.",
        "prop_sheet": None
    }
}

project["episodes"] = [
    {
        "episode": 1,
        "title": "Tập 1: Thần Khuyển Thức Tỉnh",
        "script_file": "scripts/episode_1.json",
        "source_origin": "none",
        "script_status": "generated",
        "status": "scripted",
        "item_count": 6,
        "duration_seconds": 60,
        "storyboards": {
            "total": 6,
            "available": 0,
            "stale": 0
        },
        "videos": {
            "total": 6,
            "available": 0,
            "stale": 0
        }
    }
]

project["overview"] = {
    "synopsis": "Một tổng tài kinh doanh thiên tài sau khi qua đời bất ngờ trùng sinh vào thân xác một chú chó Samoyed con và thức tỉnh hệ thống Thần Khuyển. Để sinh tồn và báo đáp chủ nhân mới tốt bụng, chú chó phải dùng trí tuệ kiếp trước hoàn thành các nhiệm vụ oái oăm giúp cô trả món nợ 100 tỷ trong 30 ngày.",
    "genre": "Trùng sinh · Hài hước · Hệ thống · Kịch tính",
    "theme": "Nghị lực vươn lên dù ở bất kỳ hình hài nào, tình cảm gia đình ấm áp",
    "world_setting": "Thế giới đô thị hiện đại kết hợp yếu tố hệ thống game viễn tưởng siêu nhiên hài hước."
}

with open(project_json_path, "w", encoding="utf-8") as f:
    json.dump(project, f, ensure_ascii=False, indent=2)

print("Updated project.json successfully.")

# 3. Validate complete project dir
validator = DataValidator()
result = validator.validate_project_dir(project_dir)
print(f"Validation Valid: {result.valid}")
if result.error_messages:
    for err in result.error_messages:
        print("Error:", err)
if result.warning_messages:
    for warn in result.warning_messages:
        print("Warning:", warn)
