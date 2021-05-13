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
        if pm.check_config():
            return  # The configuration is fresh as hell and is not ready
            # To be used to log in.

        pm.check_owner()
        pm.menu()  # Starting the interactive menu.

    except Exception as e:
        return pm.logger.error(e)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info('Exiting...')
