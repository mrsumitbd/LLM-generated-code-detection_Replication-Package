def set_global_config(config: Config):
    global GLOBAL_CONFIG
    GLOBAL_CONFIG = Config(name=config.name,
                    serve_config = config.serve_config,
                    secure_config = config.secure_config,
                    llm_config = config.llm_config,
                    log_config = config.log_config,
                    agent_config = config.agent_config,
                    router_config = config.router_config,
                    load_balancer_config = config.load_balancer_config,
                    scaling_config = config.scaling_config,
                    fault_tolerance_config = config.fault_tolerance_config
                    )