class ReActorUnload:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "trigger": {
                "type": "dict",
                "keys": {
                    "actor_id": {
                        "type": "str",
                        "required": True
                    },
                    "unload_type": {
                        "type": "str",
                        "required": True,
                        "choices": ["full", "partial"]
                    }
                }
            }
        }

    def execute(self, trigger):
        actor_id = trigger["actor_id"]
        unload_type = trigger["unload_type"]

        if unload_type == "full":
            self._full_unload(actor_id)
        elif unload_type == "partial":
            self._partial_unload(actor_id)

    def _full_unload(self, actor_id):
        # Implement full unload logic
        pass

    def _partial_unload(self, actor_id):
        # Implement partial unload logic
        pass