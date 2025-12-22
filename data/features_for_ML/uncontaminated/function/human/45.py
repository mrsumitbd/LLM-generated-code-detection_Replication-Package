import jax

def k_body(k, val):
            i_col, i_block = mat1.indices[i, k]
            chunk = jax.lax.dynamic_slice(mat2, [i_col * m, 0], (m, mat2.shape[1]))  # [m, mat2.shape[1]]
            block = mat1.data[i_block]
            return val + block.dot(chunk)