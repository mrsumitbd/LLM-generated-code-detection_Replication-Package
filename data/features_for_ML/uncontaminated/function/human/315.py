import json
from colorama import Fore
import logging
import os
from simpleval.consts import GLOBAL_CONFIG_FILE, LOGGER_NAME

def get_global_config_retries() -> RetryConfigs:
    config_file = os.path.join(os.getcwd(), GLOBAL_CONFIG_FILE)
    if os.path.exists(config_file):
        with open(config_file, 'r', encoding='utf-8') as file:
            logger = logging.getLogger(LOGGER_NAME)
            logger.info(f'{Fore.CYAN}Loading retries settings from global config{Fore.RESET}')
            config = GlobalConfigRetries(**json.load(file))
            logger.info(f'{Fore.CYAN}Retries settings: {config}{Fore.RESET}')
            return GlobalConfigRetries(**json.load(file)).retry_configs

    return GlobalConfigRetries(retry_configs=RetryConfigs()).retry_configs