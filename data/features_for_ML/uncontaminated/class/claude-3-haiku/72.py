class TopHoldersResourceWithStreamingResponse:
    def __init__(self, top_holders: TopHoldersResource) -> None:
        self.top_holders = top_holders

    def get_top_holders(self, contract_address: str, limit: int = 10, offset: int = 0) -> Iterator[TopHolderResponse]:
        top_holders = self.top_holders.get_top_holders(contract_address, limit, offset)
        for holder in top_holders:
            yield TopHolderResponse(
                address=holder.address,
                balance=holder.balance,
                rank=holder.rank
            )

class TopHolderResponse:
    def __init__(self, address: str, balance: float, rank: int) -> None:
        self.address = address
        self.balance = balance
        self.rank = rank