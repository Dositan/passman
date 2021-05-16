import re

from passman.core import create_logger, STRONG_PASSWORD
from .errors import TooWeakPassword

__all__ = ('PasswordStrength',)


class PasswordStrength:
    """The basic class to check the strength of a password."""

    def __init__(self):
        self.logger = create_logger(self.__class__.__name__)
        self.pattern = re.compile(STRONG_PASSWORD)

    def check(self, password: str):
        if self.pattern.match(password):
            return True

        return TooWeakPassword(password)
