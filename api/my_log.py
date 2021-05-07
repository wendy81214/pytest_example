"""User defined logging config."""
import logging


def config_logger(log_name):
    """Define some settings for logger."""

    logger = logging.getLogger(log_name)
    logger.setLevel(logging.DEBUG)

    format = '%(asctime)s - %(levelname)s -%(name)s : %(message)s'
    formatter = logging.Formatter(format)
    streamhandler = logging.StreamHandler()
    streamhandler.setFormatter(formatter)
    logger.addHandler(streamhandler)

    logfile = './' + log_name + '.log'
    filehandler = logging.FileHandler(logfile, mode='a')
    filehandler.setFormatter(formatter)
    logger.addHandler(filehandler)
    return logger
