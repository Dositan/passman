__all__ = ("WrongChoice", "LengthNotInRange", "NotOwner")


class BaseError(Exception):
    """The base exception for all other exceptions of this project."""


class PasswordError(BaseError):
    """Base exception for password-related errors."""


class UserError(BaseError):
    """Base exception for all user-related errors."""


class NotOwner(UserError):
    """Gets raised when the user fails the owner check."""


class WrongChoice(UserError):
    """Execption gets raised when the user does not provide

    any of the expected choices, e.g yes/no or +/-
    """


class LengthNotInRange(PasswordError):
    """Exception raised when the given length was too big."""

    def __init__(self, length: int):
        super().__init__(f"Length is not in (4, 50) range. ({length} given).")
