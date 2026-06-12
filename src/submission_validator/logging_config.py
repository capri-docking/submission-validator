import logging
import sys

_COLORS = {
    logging.DEBUG: "\033[36m",  # cyan
    logging.INFO: "\033[32m",  # green
    logging.WARNING: "\033[33m",  # yellow
    logging.ERROR: "\033[31m",  # red
    logging.CRITICAL: "\033[1;31m",  # bold red
}
_RESET = "\033[0m"


class ColorFormatter(logging.Formatter):
    """Formatter that colors the level name based on severity, when writing to a tty."""

    def __init__(self, *args, use_color: bool | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.use_color = sys.stderr.isatty() if use_color is None else use_color

    def format(self, record: logging.LogRecord) -> str:
        message = super().format(record)
        if not self.use_color:
            return message
        color = _COLORS.get(record.levelno, "")
        return f"{color}{message}{_RESET}" if color else message


def configure_logging(verbose: bool = False) -> None:
    """Configure the package-wide logger with a colored stderr handler."""
    logger = logging.getLogger("submission_validator")
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)

    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(ColorFormatter("%(levelname)s: %(message)s"))

    logger.handlers.clear()
    logger.addHandler(handler)
    logger.propagate = False
