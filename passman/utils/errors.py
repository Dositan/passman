from typing import Union


class BaseException(Exception):
    """The base exception for all other exceptions of this module."""

    def __init__(self, message: str, argument: Union[str, int] = None):
        self.message = message.format(argument)

    def __str__(self):
        return f'❌ {self.message}'


class NotOwner(BaseException):
    """Exception raised when the user fails the owner check."""

    def __init__(self):
        super().__init__('You do not own this app. Exploding...')


class LengthNotInRange(BaseException):
    """Exception raised when the given length was too big."""

    def __init__(self, length: int):
        super().__init__('Length is not in (4, 50) range. ({} given).', length)


class TooWeakPassword(BaseException):
    """Exception is raised when the given password seemed too weak."""

    def __init__(self, password: str):
        super().__init__('This password ({}) is too weak.', password)
