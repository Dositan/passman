from passman import Arguments, PasswordManager, __version__, create_logger

APP_INFO = f'''
Passman v{__version__} - made with love by Dosek for users.
The advantages of choosing passman:
  1. It is open-source.
  2. It is safe since the data is stored in the local database.
  3. There aren't any better terminal-specialized password managing apps existing.
  4. Passman gets updated every day so you won't miss new features.
'''

logger = create_logger('passman')
parser = Arguments()
parser.add('--setup', 'Whether to set the owner name with the password.')
parser.add('--info', 'See some detailed info about the application.')


def main():
    """The heart of this application."""
    pm = PasswordManager()
    args = parser.parse()

    if args.pop('info'):
        return print(APP_INFO)

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
    except KeyboardInterrupt:  # CTRL-C
        logger.info('Exiting...')
        # Notify that the program is exiting instead of sending
        # the exception that users will not understand.
