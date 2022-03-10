"""
This class handles logging for fault_bot using the logging package.

"""

# Imports
import logging


def setup_logger(log_file_name, logger_name):
    """Sets up logging for info."""
    logging.basicConfig(filename=f"{log_file_name}", format="(%(process)d) %(asctime)s [%(levelname)s] - %(name)s - %(message)s", level=logging.INFO)
    logger = logging.getLogger(logger_name)
    return logger

