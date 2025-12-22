import jax.numpy as jnp
import trax.layers.base as tl

def chunk_kkt_inv_ut_fused_kernel(
    k,
    v,
    beta,
    g,
    cu_seqlens,
    chunk_indices,
    A,
    g_cumsum,
    Ai,
    w,
    u,
    T,
    NT,
    H: tl.constexpr,
    K: tl.constexpr,
    V: tl.constexpr,
    BT: tl.constexpr,
    BK: tl.constexpr,
    BV: tl.constexpr,
    USE_G: tl.constexpr = True,
):
    B = k.shape[0]
    for b in range(B):
        for t in range(T):
            for h in range(H):
                for i in range(BT):
                    A[b, t, h, i] = jnp.dot(k[b, t, h], v[b, t, chunk_indices[b, t, h, i]])
                    g_cumsum[b, t, h, i] = g[b, t, h, i] if i == 0 else g_cumsum[b, t, h, i - 1] + g[b, t, h, i]
                    Ai[b, t, h, i] = A[b, t, h, i] + beta * g_cumsum[b, t, h, i]
                    if USE_G:
                        w[b, t, h, i] = jnp.dot(Ai[b, t, h, i], cu_seqlens[b, t, h])
                    u[b, t, h, i] = jnp.dot(Ai[b, t, h, i], cu_seqlens[b, t, h]) if USE_G else jnp.dot(Ai[b, t, h, i], cu_seqlens[b, t, h])
    return A, g_cumsum, Ai, w, u