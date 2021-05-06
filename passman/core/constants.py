from pathlib import Path

__all__ = (
    'MENU_INFO',
    'PATH',
    'HOME_DIR',
    'BASE',
    'NUMBERS',
    'UPPERCASE',
    'SPECIAL',
    'DASH_TIMES',
)

# Database-config part.
MENU_INFO = '''\tWelcome to the passman menu.
Currently-supported features:
1. Generate the password.
2. Save the password.
3. Show all the data stored in the database.
4. Export all of your passwords.'''
PATH = './passman/data'
HOME_DIR = str(Path.home())

# Password managing part.
BASE = 'qwertyuiopasdfghjklzxcvbnm'
NUMBERS = '1234567890'
UPPERCASE = 'QWERTYUIOPASDFGHJKLZXCVBNM'
SPECIAL = '!@#$%^&*()'
DASH_TIMES = 40  # this is like '*' * 40 to design the menu a bit.
