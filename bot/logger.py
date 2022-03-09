"""
This class handles logging for fault_bot using the logging package.

"""

# Imports
import logging


def setup_info(file_name):
    """Sets up logging for info."""
    logging.basicConfig(filename=f"{file_name}", format="[%(process)d] %(asctime)s - %(message)s", level=logging.INFO)


def info(log_message):
    """Logs an info message with logging."""
    logging.info(log_message)


def setup_error(file_name):
    """Sets up logging for bugs."""
    logging.basicConfig(filename=f"{file_name}", format="[%(process)d] %(asctime)s - %(message)s", level=logging.ERROR)


def error(log_message):
    """Logs an error message in the log."""
    logging.error(log_message)
