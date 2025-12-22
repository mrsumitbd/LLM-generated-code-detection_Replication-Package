def initialize_app(param: ApplicationConfig, args: List[str] = None):
    """Initialize app
    If you use gunicorn as a process manager, initialize_app can be invoke in
    `on_starting` hook.
    Args:
        param: ApplicationConfig
        args: List[str]
    """
    # Load configuration from the provided ApplicationConfig object
    config = param.load_config()

    # Set up logging
    logging.basicConfig(
        level=config.log_level,
        format=config.log_format,
        handlers=[
            logging.FileHandler(config.log_file),
            logging.StreamHandler()
        ]
    )

    # Initialize the application
    app = create_app(config)

    # Register blueprints or other application components
    register_blueprints(app)
    register_extensions(app)

    # Perform any other necessary initialization tasks
    if args:
        handle_command_line_args(app, args)

    return app