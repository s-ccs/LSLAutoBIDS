# config_logger.py
import logging
import os
from lsl_autobids.config_globals import bids_root
_logger = None  # Private variable to hold the shared logger


def get_logger(project_name: str) -> logging.Logger:
    """Initializes and returns a shared logger instance.

    Args:
        project_name (str): The name of the project.
        project_root (str): The root directory of the project.

    Returns:
        logging.Logger: Configured logger instance.
    """
    global _logger

    if _logger is not None:
        return _logger  # Return existing logger if already set

    # Create or get the logger
    _logger = logging.getLogger('shared_logger')
    _logger.setLevel(logging.DEBUG)  # Accept all logs at DEBUG level and above

    if not _logger.handlers:
        log_path = os.path.join(bids_root, project_name, "code",f"{project_name}.log")
        # Ensure the directory exists
        os.makedirs(os.path.dirname(log_path), exist_ok=True)

        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        _logger.addHandler(file_handler)

    return _logger
