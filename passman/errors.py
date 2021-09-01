__all__ = ("WrongChoice", "LengthNotInRange", "NotOwner")


class BaseError(Exception):
    """The base exception for all other exceptions of this project."""


class PasswordError(BaseError):
    """Base exception for password-related errors."""


class UserError(BaseError):
    """Base exception for all user-related errors."""


class NotOwner(UserError):
    """Gets raised when the user fails the owner check."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class WrongChoice(UserError):
    """Execption gets raised when the user does not provide

    any of the expected choices, e.g yes/no or +/-
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class LengthNotInRange(PasswordError):
    """Exception raised when the given length was too big."""

    def __init__(self, length: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.length = length

    def __str__(self):
        return f"Length is not in (4, 50) range. ({self.length} given)."
