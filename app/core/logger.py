import logging
from logging.handlers import RotatingFileHandler
from fastapi import Request
import os
from core import settings

log_level = getattr(logging, settings.log_level)

# Ensure the log directory exists
if not os.path.exists(settings.log_dir):
    os.makedirs(settings.log_dir)

# Set up the logger (set name to the calling module)
logger = logging.getLogger(__name__)
logger.setLevel(log_level)

# Create a file handler that logs messages to a file with rotation
file_handler = RotatingFileHandler(os.path.join(settings.log_dir, settings.log_file), maxBytes=settings.log_max_file_size_bytes, backupCount=settings.log_max_files)
file_handler.setLevel(log_level)

# Create a console handler that logs messages to the console (optional)
console_handler = logging.StreamHandler()
console_handler.setLevel(log_level)

# Define the logging format
formatter = logging.Formatter(settings.log_format)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Log exceptions
def log_exception(request: Request, exc: Exception) -> None:
    logger.error(f"Exception occurred in {request.url.path}: {exc}")
    logger.exception(exc)
