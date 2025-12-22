def init_logging(args: Args) -> None:
    import logging

    logging.basicConfig(level=args.log_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')