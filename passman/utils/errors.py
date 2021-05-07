
class NotOwner(Exception):
    """Exception raised when the user fails the owner check."""

    def __init__(self, message: str = 'You do not own this app. Exploding...'):
        self.message = message

    def __str__(self):
        return f'❌ {self.message}'


class LengthNotInRange(Exception):
    """Exception raised when the given length was too big."""

    def __init__(self, length: int, message: str = 'Length is not in (4, 50) range.'):
        super().__init__(message)
        self.length = length
        self.message = message

    def __str__(self):
        return f'❌ {self.message} ({self.length} given).'


class TooWeakPassword(Exception):
    """TODO: exception should be raised on password check.
    Check for:
    1. length;
    2. character types;
    """
    ...
