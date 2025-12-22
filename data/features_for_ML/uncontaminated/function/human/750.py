import time
import requests
from mist.app.loggers.logger import logger

def retrieve_page_data(
        url: str, retries: int = 3, timeout: int = 60 * 5
    ) -> requests.Response:
        """
        Retrieves data from the given URL.
        :param url: URL
        :param retries: Number of retries
        :param timeout: Timeout (in seconds)
        :return: URL data
        """
        error = None
        for retry in range(retries):
            try:
                response = requests.get(url, timeout=timeout)
                response.raise_for_status()
                return response
            except BaseException as err:
                logger.warning(
                    f'Error retrieving page data ({err}), retrying (attempt {retry + 1})'
                )
                error = err
                time.sleep(1)
        raise RuntimeError(f'Error retrieving page data: {url}: {error}')