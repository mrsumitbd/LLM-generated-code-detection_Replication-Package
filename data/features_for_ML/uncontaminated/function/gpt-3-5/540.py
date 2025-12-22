def create(
        *,
        num_stages: int,
        producer_group: CooperativeGroup,
        consumer_group: CooperativeGroup,
        tx_count: int,
        barrier_storage: cute.Pointer = None,
        cta_layout_vmnk: Optional[cute.Layout] = None,
        tidx: Optional[Int32] = None,
    ):
        return PipelineTmaAsync(
            num_stages=num_stages,
            producer_group=producer_group,
            consumer_group=consumer_group,
            tx_count=tx_count,
            barrier_storage=barrier_storage,
            cta_layout_vmnk=cta_layout_vmnk,
            tidx=tidx
        )