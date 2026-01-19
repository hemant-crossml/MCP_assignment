"""
logger_config.py
----------------
Centralized logging configuration for the entire project.
Provides consistent logging format, levels, and handlers across all modules.

IMPORTANT:
- STDOUT is reserved for JSON-RPC communication (MCP protocol)
- All logs MUST go to STDERR or files
"""

import logging
import sys
from logging.handlers import RotatingFileHandler
from datetime import datetime


def setup_logger(
    name: str,
    log_file: str = "agent_app.log",
    level: int = logging.DEBUG
) -> logging.Logger:
    """
    Summary:
        Creates and configures a logger with file and stderr console handlers.

    Args:
        name: Logger name (typically __name__ of the calling module)
        log_file: Path to log file
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    # Detailed formatter (file)
    detailed_formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console formatter (stderr)
    console_formatter = logging.Formatter(
        fmt="%(levelname)-8s | %(name)s | %(message)s"
    )

    # File handler (rotating)
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)

    # 🚨 CRITICAL FIX: log to STDERR, NOT STDOUT
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# Default application logger
app_logger = setup_logger("agent_app")
app_logger.info("=" * 50)
app_logger.info("Logging system initialized (STDIO-safe)")
app_logger.info(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
app_logger.info("=" * 50)
