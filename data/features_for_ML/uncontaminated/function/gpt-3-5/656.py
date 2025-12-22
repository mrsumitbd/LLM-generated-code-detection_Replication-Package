def create_reduce_scater_2d_ctx(max_M, N, rank, world_size, local_world_size, dtype, overlap_with_gemm=True,
                                num_reduction_sms=15):
    class ReduceScatter2DContext:
        def __init__(self, max_M, N, rank, world_size, local_world_size, dtype, overlap_with_gemm, num_reduction_sms):
            self.max_M = max_M
            self.N = N
            self.rank = rank
            self.world_size = world_size
            self.local_world_size = local_world_size
            self.dtype = dtype
            self.overlap_with_gemm = overlap_with_gemm
            self.num_reduction_sms = num_reduction_sms

    return ReduceScatter2DContext(max_M, N, rank, world_size, local_world_size, dtype, overlap_with_gemm, num_reduction_sms)