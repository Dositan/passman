import argparse

__all__ = ('Arguments',)


class DefaultArguments(argparse.ArgumentParser):
    """Default Argument class with a couple of overridden methods."""

    def __init__(self, message: str = 'Put some arguments beforehand.'):
        super().__init__(message)

    def error(self, message: str):
        raise RuntimeError(message)


class Arguments(DefaultArguments):
    """The Password Arguments class to ease up the flag creation process."""

    def add(self, name: str, description: str = 'No help given.') -> None:
        """The custom implementation of ArgumentParser.add_argument

        to ease up the flags creation process.

        Args:
            name (str): The name of the flag.
            description (str, optional): The help for the flag. Defaults to 'No help given.'.
        """
        self.add_argument(name, default=False, action='store_true', help=description)

    def parse(self) -> dict:
        """The kind of not recommended implementationof ArgumentParser.parse_args.

        It is used to convert Namespace object into dict directly.

        This helps to iterate the dict object like **kwargs.

        Returns:
            dict: Namespace → dict flags.
        """
        return self.parse_args().__dict__
