
class NeMoRLOpenAIChatRequestMixin:
            def model_post_init(self, context):
                # Penguin specific processing. This is just how Penguin returns the extra token information.
                if self.required_prefix_token_ids is None:
                    for message in reversed(self.messages):
                        if "prompt_token_ids" in message:
                            self.required_prefix_token_ids = (
                                message["prompt_token_ids"]
                                + message["generation_token_ids"]
                            )
                            break

                return super().model_post_init(context)