def sequence_mask(length, max_length=None):
    import tensorflow as tf
    return tf.sequence_mask(length, max_length)