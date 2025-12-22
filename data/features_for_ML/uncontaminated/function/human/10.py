from logging import (
    DEBUG,
    INFO,
    Formatter,
    Logger,
    StreamHandler,
    basicConfig,
    captureWarnings,
    getLogger,
)
from streetrace.args import Args
import litellm
import litellm

def init_logging(args: Args) -> None:
    """Initialize logging for the application.

    Should be called once when the application starts.
    """
    # --- Logging Configuration ---
    # Basic config for file logging
    basicConfig(
        level=INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        filename="streetrace.log",
        filemode="w",
    )

    captureWarnings(True)  # noqa: FBT003

    # Console handler for user-facing logs
    console_handler = StreamHandler()
    console_handler.setLevel(INFO)
    console_formatter = Formatter("%(levelname)s: %(message)s")
    console_handler.setFormatter(console_formatter)

    root_logger = getLogger()
    configure_3p_loggers(root_logger)

    # Configure Logging Level based on args
    if args.verbose:
        import litellm

        # https://docs.litellm.ai/docs/debugging/local_debugging
        litellm._turn_on_debug()  # type: ignore[attr-defined,no-untyped-call] # noqa: SLF001
        # Add console handler only if debug is enabled
        # Root logger setup
        # Set root logger level to DEBUG initially to capture everything
        root_logger.setLevel(DEBUG)
        root_logger.info("Debug logging enabled.")
        __verbose_logging = True
    # --- End Logging Configuration ---