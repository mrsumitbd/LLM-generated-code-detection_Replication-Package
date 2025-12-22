from typing import List
from dataclasses import dataclass

@dataclass
class TopHolder:
    name: str
    holdings: float

class TopHoldersResource:
    def __init__(self, top_holders: List[TopHolder]) -> None:
        self.top_holders = top_holders

class TopHoldersResourceWithStreamingResponse:

    def __init__(self, top_holders: TopHoldersResource) -> None:
        self.top_holders = top_holders