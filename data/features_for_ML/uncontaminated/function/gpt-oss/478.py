import logging

# Configure a basic logger if one hasn't been configured elsewhere
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def on_download_complete(success, message):
    """
    Callback invoked when a download operation finishes.

    Parameters
    ----------
    success : bool
        True if the download succeeded, False otherwise.
    message : str
        A human‑readable message describing the outcome or error.
    """
    if success:
        logger.info(f"Download completed successfully: {message}")
    else:
        logger.error(f"Download failed: {message}")