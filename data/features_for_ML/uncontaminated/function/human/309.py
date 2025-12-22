def get_default_group_cast_config(num_ranks: int) -> "GrpCollConfig":
        """
        Get a recommended dispatch config.

        Argument:
            num_ranks: the number of ranks.

        Returns:
            config: the recommended config.
        """

        # TODO: automatically tune
        config_map = {
            2: GrpCollConfig(24, 24, 256, 6, 128),
            4: GrpCollConfig(24, 6, 256, 6, 128),
            8: GrpCollConfig(24, 6, 256, 6, 128),
            16: GrpCollConfig(24, 36, 288, 20, 128),
            24: GrpCollConfig(24, 8, 288, 32, 128),
            32: GrpCollConfig(24, 32, 288, 32, 128),
            64: GrpCollConfig(24, 20, 288, 28, 128),
            128: GrpCollConfig(24, 20, 560, 32, 128),
            144: GrpCollConfig(24, 32, 720, 12, 128),
            160: GrpCollConfig(24, 28, 720, 12, 128),
        }
        assert num_ranks in config_map, f"Unsupported number of ranks: {num_ranks}"
        return config_map[num_ranks]