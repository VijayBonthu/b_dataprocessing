import logging
import os
from logging.handlers import TimedRotatingFileHandler


def setup_logger(service_name):
    home_dir = os.path.expanduser('~')

    log_dir = os.path.join(home_dir, "logs")

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file = os.path.join(log_dir, f"{service_name}_logs.log")

    logger = logging.getLogger(service_name)
    logger.setLevel(logging.INFO)

    handler = TimedRotatingFileHandler(log_file, when='midnight', interval=1, backupCount=7)
    handler.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger
