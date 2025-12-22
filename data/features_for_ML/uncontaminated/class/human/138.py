import asyncio

class Response:
                def __init__(self, response_id: str, *, use_elevenlabs: bool | None = None):
                    if use_elevenlabs is None:
                        use_elevenlabs = False
                    self.response_id = response_id
                    if use_elevenlabs:
                        self.text_delta_queue: asyncio.Queue = asyncio.Queue()
                        self.text_delta_task = asyncio.create_task(process_text_deltas(self))