"""File containing logger class and functions"""

from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL
from logging import Formatter, LogRecord, Logger, StreamHandler, FileHandler
from logging import getLogger


class LoggingFormatter(Formatter):
    """Logging formatter for server"""
    # Colors
    BLACK = "\x1b[30m"
    RED = "\x1b[31m"
    GREEN = "\x1b[32m"
    YELLOW = "\x1b[33m"
    BLUE = "\x1b[34m"
    GRAY = "\x1b[38m"
    # Styles
    RESET = "\x1b[0m"
    BOLD = "\x1b[1m"

    COLORS: dict[int, str] = {
        DEBUG: GRAY + BOLD,
        INFO: BLUE + BOLD,
        WARNING: YELLOW + BOLD,
        ERROR: RED,
        CRITICAL: RED + BOLD,
    }

    def format(self, record: LogRecord) -> str:
        LOG_COLOR: str = self.COLORS[record.levelno]
        new_format: str = "(black){asctime}(reset) (levelcolor){levelname:<8}(reset) (green){name}(reset) {message}"
        new_format = new_format.replace("(black)", self.BLACK + self.BOLD)
        new_format = new_format.replace("(reset)", self.RESET)
        new_format = new_format.replace("(levelcolor)", LOG_COLOR)
        new_format = new_format.replace("(green)", self.GREEN + self.BOLD)
        formatter = Formatter(new_format, "%Y-%m-%d %H:%M:%S", style="{")
        return formatter.format(record)


def assemble_logger() -> Logger:
    """Assembles and returns bot server logger"""
    LOGGER: Logger = getLogger("Mobius")
    LOGGER.setLevel(INFO)

    # Console handler
    CONSOLE_HANDLER = StreamHandler()
    CONSOLE_HANDLER.setFormatter(LoggingFormatter())
    # File handler
    FILE_HANDLER = FileHandler(
        filename="discord.log", encoding="utf-8", mode="w")
    FILE_HANDLER_FORMATTER = Formatter(
        "[{asctime}] [{levelname:<8}] {name}: {message}", "%Y-%m-%d %H:%M:%S", style="{")
    FILE_HANDLER.setFormatter(FILE_HANDLER_FORMATTER)

    # Add the handlers
    LOGGER.addHandler(CONSOLE_HANDLER)
    LOGGER.addHandler(FILE_HANDLER)

    return LOGGER
