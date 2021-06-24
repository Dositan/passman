import logging
import sys

from passman.cli import parse_early_exit_flags, parse_flags
from passman.core.manager import PasswordManager

log = logging.getLogger('passman.main')


def main():
    """The heart of this application."""
    # Beforehand flag-parsing.
    args = parse_flags(sys.argv[1:])
    parse_early_exit_flags(args)

    manager = PasswordManager()
    if args.setup:
        manager.setup()
        sys.exit(0)

    try:
        if manager.check_config():
            sys.exit(0)  # The configuration is fresh as hell and is not ready
            # To be used to log in.

        manager.check_owner()
        manager.menu()  # Starting the interactive menu.

        if args.reset_config:
            manager.reset_config()

    except KeyboardInterrupt:  # CTRL-C
        log.info('Exiting...')
        # Notify that the program is exiting instead of sending
        # the exception that users will not even understand.
        sys.exit(0)

    except Exception as exc:
        log.error(exc)
        sys.exit(1)  # Because of an unhandled exception.


if __name__ == '__main__':
    main()
