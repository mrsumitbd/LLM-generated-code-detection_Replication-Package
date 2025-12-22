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
    """
    This helper function computes any necessary attributes and returns an instance of PipelineTmaAsync.
    :param barrier_storage: Pointer to the smem address for this pipeline's mbarriers
    :type barrier_storage: cute.Pointer
    :param num_stages: Number of buffer stages for this pipeline
    :type num_stages: Int32
    :param producer_group: CooperativeGroup for the producer agent
    :type producer_group: CooperativeGroup
    :param consumer_group: CooperativeGroup for the consumer agent
    :type consumer_group: CooperativeGroup
    :param tx_count: Number of bytes expected to be written to the transaction barrier for one stage
    :type tx_count: int
    :param cta_layout_vmnk: Layout of the cluster shape
    :type cta_layout_vmnk: cute.Layout | None
    :param tidx: thread index to consumer async threads
    :type tidx: Int32 | None
    """
    return PipelineTmaAsync(
        num_stages=num_stages,
        producer_group=producer_group,
        consumer_group=consumer_group,
        tx_count=tx_count,
        barrier_storage=barrier_storage,
        cta_layout_vmnk=cta_layout_vmnk,
        tidx=tidx,
    )