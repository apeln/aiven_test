import logging
import logging.handlers
from pathlib import Path

def get_logger(log_file_name):
    filename = Path(log_file_name)
    filename.touch(exist_ok=True)  #  create file if not exists

    # Logger creation
    logger = logging.getLogger(__name__)  
    # set log level
    logger.setLevel(logging.INFO)
    # define file handler and set formatter
    file_handler = logging.FileHandler(log_file_name)
    formatter    = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
    file_handler.setFormatter(formatter)
    # add file handler to logger
    logger.addHandler(file_handler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(formatter)
    logger.addHandler(consoleHandler)

    return logger