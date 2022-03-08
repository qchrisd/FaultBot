"""
This class handles logging for fault_bot using the logging package.

"""

# Imports
import logging


def setup_logging(file_name):
    """Sets up logging."""
    logging.basicConfig(filename=f"{file_name}", format="[%(process)d] %(asctime)s - %(message)s", level=logging.INFO)


def log_info(log_message):
    """Logs a message with logging."""
    logging.info(log_message)