from scripts.reactor_swapper import (
    unload_all_models,
)

class ReActorUnload:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "trigger": ("IMAGE", ),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "execute"
    CATEGORY = "🌌 ReActor"

    def execute(self, trigger):
        unload_all_models()
        return (trigger,)