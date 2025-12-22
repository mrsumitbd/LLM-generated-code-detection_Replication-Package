class ReActorUnload:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "trigger": ("BOOLEAN", {"default": False}),
            }
        }

    def execute(self, trigger):
        if trigger:
            import sys
            if 'reactor' in sys.modules:
                del sys.modules['reactor']
            if 'cv2' in sys.modules:
                del sys.modules['cv2']
            if 'insightface' in sys.modules:
                del sys.modules['insightface']
        
        return ()