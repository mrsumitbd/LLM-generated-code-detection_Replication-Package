def create_and_permute_tensor(l, mode0, mode1, is_mode0_major, dtype, is_dynamic_layout=True):
    import tensorflow as tf
    
    if is_mode0_major:
        tensor = tf.random.uniform((l, mode1, mode0), dtype=dtype)
        permuted_tensor = tf.transpose(tensor, perm=[2, 1, 0])
    else:
        tensor = tf.random.uniform((l, mode0, mode1), dtype=dtype)
        permuted_tensor = tf.transpose(tensor, perm=[1, 2, 0])
    
    return permuted_tensor