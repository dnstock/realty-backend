import logging
from logging.handlers import RotatingFileHandler
from fastapi import Request
from pathlib import Path
from core import settings

# Set up the log level
log_level = getattr(logging, settings.log_level.upper(), logging.INFO)

# Ensure the log directory exists
log_dir = Path(settings.log_dir)
log_dir.mkdir(parents=True, exist_ok=True)

# Initialize the logger for the calling module
logger = logging.getLogger(__name__)
logger.setLevel(log_level)

# Create rotating file handler for log rotation
file_handler = RotatingFileHandler(
    log_dir / settings.log_file,
    maxBytes=settings.log_max_file_size_bytes,
    backupCount=settings.log_max_files
)
file_handler.setLevel(log_level)

# Create console handler for logging to stdout
console_handler = logging.StreamHandler()
console_handler.setLevel(log_level)

# Define the logging format
formatter = logging.Formatter(settings.log_format)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to the logger only if not already added
if not logger.hasHandlers():
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

# Log exceptions
async def log_exception(request: Request, exc: Exception) -> None:
    logger.error(f"Exception occurred in {request.url.path}: {exc}", exc_info=True)
