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
            }
        }

    RETURN_TYPES = ("whisper_alignment",)
    RETURN_NAMES = ("alignment",)
    FUNCTION = "string_to_alignment"
    CATEGORY = "whisper"

    def string_to_alignment(self, alignment_str):
        """
        alignment_str:
        "[{'value':'123','start':0.1,'end':0.2}]"
        """

        try:
            # 安全地把字符串转成 Python 对象
            alignment = ast.literal_eval(alignment_str)

            if not isinstance(alignment, list):
                raise ValueError("Parsed alignment is not a list")

        except Exception as e:
            raise RuntimeError(f"Failed to parse whisper_alignment: {e}")

        return (alignment,)
