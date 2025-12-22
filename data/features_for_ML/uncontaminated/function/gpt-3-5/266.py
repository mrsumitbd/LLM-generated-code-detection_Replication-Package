import numpy as np
import cupy as cp

def dtw_cuda(x, BLOCK_SIZE=1024):
    x = cp.asarray(x)
    n = x.shape[0]
    cost = cp.zeros((n, n), dtype=cp.float32)
    
    @cp.fuse
    def dist(a, b):
        return cp.abs(a - b)
    
    for i in range(n):
        for j in range(n):
            cost[i, j] = dist(x[i], x[j])
    
    D = cp.zeros((n, n), dtype=cp.float32)
    D[0, 0] = cost[0, 0]
    
    for i in range(1, n):
        D[i, 0] = cost[i, 0] + D[i-1, 0]
        D[0, i] = cost[0, i] + D[0, i-1]
    
    for i in range(1, n):
        for j in range(1, n):
            D[i, j] = cost[i, j] + cp.minimum(D[i-1, j], cp.minimum(D[i, j-1], D[i-1, j-1]))
    
    return D[n-1, n-1].get()