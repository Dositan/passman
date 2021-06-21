import logging
import sys

__all__ = ('init_logging',)


def init_logging(level: int) -> None:
    """The logger initializing method used to ease up the logging manipulation.

    Args:
        level (int): The minimal logging level.
    """
    root = logging.getLogger()

    base = logging.getLogger('passman')
    base.setLevel(level)

    warnings = logging.getLogger('py.warnings')
    warnings.setLevel(logging.WARNING)

    file_formatter = logging.Formatter(
        '[{asctime}] [{levelname}] {name}: {message}',
        datefmt='%Y-%m-%d %H:%M:%S',
        style='{'
    )
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(file_formatter)

    root.addHandler(handler)
    logging.captureWarnings(True)
