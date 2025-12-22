from typing import Optional
import cutlass.cute as cute
from cutlass import Boolean, Int32, const_expr
from cutlass.pipeline import MbarrierArray, CooperativeGroup, PipelineOp, pipeline_init_wait
from cutlass.pipeline import PipelineAsync, PipelineTmaAsync, PipelineState, PipelineUserType

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
        if not isinstance(barrier_storage, cute.Pointer):
            raise ValueError(
                f"Expected barrier_storage to be a cute.Pointer, but got {type(barrier_storage)}"
            )

        producer_type = PipelineOp.TmaLoad
        consumer_type = PipelineOp.AsyncThread

        producer = (producer_type, producer_group)
        consumer = (consumer_type, consumer_group)

        sync_object_full = PipelineAsync._make_sync_object(
            barrier_storage.align(min_align=8), num_stages, producer, tx_count
        )
        sync_object_empty = PipelineAsync._make_sync_object(
            barrier_storage.align(min_align=8) + num_stages, num_stages, consumer
        )
        if tidx is None:
            tidx, _, _ = cute.arch.thread_idx()
        if cta_layout_vmnk is None:
            cta_layout_vmnk = cute.make_layout((1, 1, 1, 1))
        (
            dst_rank,
            is_signalling_thread,
        ) = PipelineTmaAsync.init_empty_barrier_arrive_signal(cta_layout_vmnk, tidx)
        if cta_layout_vmnk is None or cute.size(cta_layout_vmnk) == 1:
            dst_rank = None
        else:
            dst_rank = dst_rank

        producer_mask = None

        pipeline_init_wait(cta_layout_vmnk)

        return PipelineTmaCpAsync(
            sync_object_full,
            sync_object_empty,
            num_stages,
            producer_mask,
            dst_rank,
            is_signalling_thread,
        )