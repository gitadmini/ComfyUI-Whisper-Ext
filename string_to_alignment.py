import ast

class StringToWhisperAlignmentNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "alignment_str": ("STRING", {
                    "multiline": True,
                    "default": "[{'value':'123','start':0.1,'end':0.2}]"
                }),
                "video_duration": ("FLOAT", {"forceInput": True}),
            }
        }

    RETURN_TYPES = ("whisper_alignment",)
    RETURN_NAMES = ("alignment",)
    FUNCTION = "string_to_alignment"
    CATEGORY = "whisper"

    def string_to_alignment(self, alignment_str, video_duration):
        """
        alignment_str 示例:
        "[{'value':'Once we met','start':0,'end':2.635},
          {'value':'no three minutes','start':2.72,'end':2.72}]"
        """

        try:
            # 安全地把字符串转成 Python 对象
            alignment = ast.literal_eval(alignment_str)

            if not isinstance(alignment, list):
                raise ValueError("Parsed alignment is not a list")

            # 修正 end > video_duration 的情况
            for item in alignment:
                if not isinstance(item, dict):
                    continue

                if "end" in item and isinstance(item["end"], (int, float)):
                    if item["end"] > video_duration:
                        item["end"] = video_duration

        except Exception as e:
            raise RuntimeError(f"Failed to parse whisper_alignment: {e}")

        return (alignment,)
