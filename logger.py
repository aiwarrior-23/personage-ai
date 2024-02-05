import logging
import os

def get_logger(name):
    """
    Get logger instance.

    Args:
    name (str): Name of the logger.

    Returns:
    Logger: Logger instance.
    """
    # Set up the logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Define the log file path
    log_file_path = os.path.join(os.path.dirname(__file__), 'logs/logs.log')

    # Create the 'logs' directory if it doesn't exist
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

    # Configure the log formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Create a FileHandler for writing log messages to the file
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Add the FileHandler to the logger
    logger.addHandler(file_handler)

    return logger
