import ast
import json


class StringToWhisperAlignmentNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "start_time": ("FLOAT", {"forceInput": True}),
                "video_duration": ("FLOAT", {"forceInput": True}),
                "alignment_str": (
                    "STRING",
                    {
                        "multiline": True,
                        "default": "[{'value':'123','start':0.1,'end':0.2}]"
                    }
                ),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("whisper_alignment_json",)
    FUNCTION = "string_to_alignment"
    CATEGORY = "whisper"

    def string_to_alignment(self, alignment_str, start_time, video_duration):
        """
        start_time + video_duration = end_time
        只保留 [start_time, end_time] 区间内的片段
        """

        end_time = start_time + video_duration

        try:
            alignment = ast.literal_eval(alignment_str)

            if not isinstance(alignment, list):
                raise ValueError("Parsed alignment is not a list")

            # 1️⃣ 只保留与区间有交集的片段
            clipped = []
            for item in alignment:
                if not isinstance(item, dict):
                    continue

                s = item.get("start")
                e = item.get("end")

                if not isinstance(s, (int, float)) or not isinstance(e, (int, float)):
                    continue

                # 无交集 → 丢弃
                if e <= start_time or s >= end_time:
                    continue

                # 裁剪到区间内
                item = item.copy()
                item["start"] = max(s, start_time)
                item["end"] = min(e, end_time)

                clipped.append(item)

            if not clipped:
                return (json.dumps([], ensure_ascii=False),)

            # 2️⃣ 所有时间减去 start_time（从 0 开始）
            for item in clipped:
                item["start"] -= start_time
                item["end"] -= start_time

        except Exception as e:
            raise RuntimeError(f"Failed to parse whisper_alignment: {e}")

        return (json.dumps(clipped, ensure_ascii=False),)
