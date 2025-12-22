import jax.numpy as jnp

def loss(log_alpha: jnp.ndarray) -> jnp.ndarray:
        alpha = jnp.exp(log_alpha)
        alpha = jnp.clip(alpha, min_disp, max_disp)

        W = mu[:, None] / (1 + mu[:, None] * alpha)
        W = jnp.clip(W, 1e-15, 1e6)

        base_loss = nb_nll_vmap(counts, mu, alpha)

        cr_term = jnp.where(
            cr_reg,
            0.5 * safe_slogdet((design_matrix.T[:, :, None] * W).transpose(2, 0, 1) @ design_matrix)[1],
            0.0,
        )

        prior_term = jnp.where(
            prior_reg,
            (jnp.log(alpha) - jnp.log(alpha_hat)) ** 2 / (2 * prior_disp_var),
            0.0,
        )

        total_loss = base_loss + cr_term + prior_term

        return jnp.where(jnp.isfinite(total_loss), total_loss, 1e15)