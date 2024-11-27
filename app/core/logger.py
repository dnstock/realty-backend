import logging
import json
from pathlib import Path
from typing import Any
from contextvars import ContextVar
from logging.handlers import RotatingFileHandler, SMTPHandler
from fastapi import Request
from core import settings

# Request ID for correlating logs to a single request
request_id_context: ContextVar[str | None] = ContextVar('request_id', default=None)

# Set up the log level dynamically from settings
log_level = getattr(logging, settings.log_level, logging.INFO)

# Ensure the log directory exists (using pathlib for cleaner handling)
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
file_handler.setLevel(getattr(logging, settings.log_level_file, log_level))  # type: ignore (handled by field validator)

# Create console handler for logging to stdout
console_handler = logging.StreamHandler()
console_handler.setLevel(getattr(logging, settings.log_level_console, log_level))  # type: ignore (handled by field validator)

# Text formatter for standard logging
text_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# JSON formatter for structured logging
class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_record: dict[str, Any] = {
            'timestamp': self.formatTime(record),
            'level': record.levelname,
            'message': record.getMessage(),
            'module': record.module,
            'filename': record.filename,
            'request_id': request_id_context.get(),
            'exception': self.formatException(record.exc_info) if record.exc_info else None,
        }
        return json.dumps(log_record)
json_formatter = JsonFormatter()

# Set the file and console formatters
file_handler.setFormatter(json_formatter if settings.log_format_file == 'json' else text_formatter)
console_handler.setFormatter(json_formatter if settings.log_format_console == 'json' else text_formatter)

# Optional: Create an SMTP handler for critical errors (e.g. email alerts)
smtp_handler = SMTPHandler(
    mailhost=(settings.smtp_server, settings.smtp_port),       # type: ignore (handled by field validator)
    fromaddr=settings.alerts_email_from,                       # type: ignore (handled by field validator)
    toaddrs=settings.alerts_email_to,                          # type: ignore (handled by field validator)
    subject='Critical Error in Application',
    credentials=(settings.smtp_user, settings.smtp_password),  # type: ignore (handled by field validator)
    secure=()
)
smtp_handler.setLevel(logging.CRITICAL)

# Add handlers to the logger only if not already added
if not logger.hasHandlers():
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    if settings.alerts_email_enabled:
        logger.addHandler(smtp_handler)

# Log exceptions
def log_exception(exc: Exception, occured_in: str | None) -> None:
    logger.error(
        exc if occured_in is None else f'Exception occurred in {occured_in}: {exc}',
        exc_info=True,
        extra={'request_id': request_id_context.get()}
    )

def log_middleware_exception(exc: Exception, request: Request) -> None:
    log_exception(exc, request.url.path)
