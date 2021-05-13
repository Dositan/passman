'''
TODO-1: create a separate class for checking the password strength
TODO-2: use the power of regular expressions
TODO-3: find the usage of the feature somewhere
'''

import re

from .errors import TooWeakPassword

__all__ = ('PasswordStrength',)


class PasswordStrength:
    """The basic class to check the strength of a password."""

    def __init__(self):
        self._pattern = re.compile('^[a-zA-Z0-9]')

    def check(self, password: str):
        if self._pattern.fullmatch(password):
            return True

        raise TooWeakPassword(password)
