import argparse

from passman import PasswordArguments, PasswordManager, create_logger

logger = create_logger('passman')
parser = PasswordArguments()
parser.add('--setup', 'Whether to set the owner name with the password.')


def main():
    """The heart of this application."""
    pm = PasswordManager()
    args = parser.parse()

    if args.pop('setup'):
        return pm.setup()

    try:
        pm.check_owner()

    except Exception as e:
        return pm.logger.error(e)

    pm.menu()  # Starting the interactive menu.


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info('Exiting...')
