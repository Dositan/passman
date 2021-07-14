import argparse
import sys

import passman

APP_INFO = f'''
Passman v{passman.__version__} - made with love by Dosek for users.
The advantages of choosing passman:
  1. It is open-source.
  2. It is safe since the data is stored in the local database.
  3. There aren't any better terminal-specialized password managing apps existing.
  4. Passman gets updated every day so you won't miss new features.
'''


def parse_early_exit_flags(args: argparse.Namespace) -> None:
    if args.info:
        print(APP_INFO)
        sys.exit(0)  # Safely exit.


def parse_flags(args: argparse.Namespace = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='passman - the Password Manager',
        usage='python -m passman [arguments]'
    )
    parser.add_argument(
        '-s',
        '--setup',
        action='store_true',
        help='Whether to set the owner name with the password.'
    )
    parser.add_argument(
        '-i',
        '--info',
        action='store_true',
        help='See some detailed info about the application.'
    )
    parser.add_argument(
        '-rc',
        '--reset-config',
        action='store_true',
        help='Whether to reset the current configuration after app exit.'
    )
    return parser.parse_args(args)
