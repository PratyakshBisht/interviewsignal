import logging
import logging.handlers
import os
from datetime import datetime


def setup_logging():
    """Configure structured logging for production."""
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    # Create formatters
    json_formatter = logging.Formatter(
        '{"timestamp": "%(asctime)s", "level": "%(levelname)s", '
        '"service": "interview-signal-api", "module": "%(name)s", '
        '"message": "%(message)s", "pathname": "%(pathname)s", '
        '"lineno": %(lineno)d}'
    )

    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s [%(pathname)s:%(lineno)d]'
    )

    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(detailed_formatter)

    # File handler - JSON logs
    current_date = datetime.now().strftime("%Y-%m-%d")
    json_handler = logging.handlers.RotatingFileHandler(
        f"{log_dir}/app-{current_date}.json",
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=30,
        encoding="utf-8",
    )
    json_handler.setLevel(logging.INFO)
    json_handler.setFormatter(json_formatter)

    # File handler - detailed logs
    detailed_handler = logging.handlers.RotatingFileHandler(
        f"{log_dir}/app-{current_date}.log",
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=30,
        encoding="utf-8",
    )
    detailed_handler.setLevel(logging.DEBUG)
    detailed_handler.setFormatter(detailed_formatter)

    # Error handler
    error_handler = logging.handlers.RotatingFileHandler(
        f"{log_dir}/errors-{current_date}.log",
        maxBytes=10 * 1024 * 1024,
        backupCount=30,
        encoding="utf-8",
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(detailed_formatter)

    # Add handlers
    root_logger.addHandler(console_handler)
    root_logger.addHandler(json_handler)
    root_logger.addHandler(detailed_handler)
    root_logger.addHandler(error_handler)

    # Third-party loggers
    for logger_name in ['uvicorn', 'gunicorn', 'sqlalchemy']:
        logging.getLogger(logger_name).setLevel(logging.WARNING)

    return root_logger


# Initialize logging
logger = setup_logging()
