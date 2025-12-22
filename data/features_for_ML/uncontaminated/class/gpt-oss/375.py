class ReActorUnload:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "trigger": ("Trigger",)
            }
        }

    def execute(self, trigger):
        # Attempt to unload the ReActor model if possible
        try:
            import reactor
            if hasattr(reactor, "unload"):
                reactor.unload()
        except Exception:
            # If the import or unload fails, silently ignore
            pass

        # Pass the trigger through unchanged
        return {"trigger": trigger}