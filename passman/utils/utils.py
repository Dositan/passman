import json
import random
from collections import Counter
from glob import glob
from typing import NoReturn

from passman.core import DatabaseManager, create_logger
from passman.core.constants import *
from passman.utils import NotOwner, PasswordStrength, TabulateData

__all__ = ('PasswordManager',)


def sinput(message: str):
    """This is just to avoid extra spaces in the user-input
    that may cause some logical problems.

    Args:
        message (str): Accordingly, a message to get input by.

    Returns:
        str: Stripped input function.
    """
    return input(message).strip()


def convert_choice(choice: str) -> bool:
    """The fast way to figure out the user choice.

    Args:
        choice (str): User-input to grab the choice from.

    Returns:
        bool: Either True or False, according to the convertation.
    """
    if choice.lower() in ('y', 'yes', '+'):
        return True

    return False


def keep_living(func):
    """A special decorator made to make endless loops for
    methods that have sense being used with a loop."""
    def inner(*args, **kwargs):
        func(*args, **kwargs)

        print(DASH_LINE)
        while convert_choice(sinput('📢 Do you want to repeat (y/n)? ')):
            func(*args, **kwargs)

    return inner


class PasswordManager:
    """The Password Manager class to manipulate with generating passwords."""

    def __init__(self):
        self.logger = create_logger(self.__class__.__name__)
        self.database = DatabaseManager()
        self.strength = PasswordStrength()

        with open(f'{PATH}/config.json') as file:
            self.config = json.load(file)

    def __dir__(self):
        return [self.generate_password, self.save_password, self.check_password,
                self.show_data, self.export_data, self.code_statistics]

    @keep_living
    def check_password(self):
        """The check password method to make user sure about their
        password strength. 

        Planned to be used everywhere the password was entered.
        """
        # TODO: use checking everywhere the password was entered.
        # FIXME: create a normal way of a password checking in ./checks.py
        password = sinput('Enter the password that should be checked: ')

        if (check := self.strength.check(password)) is True:
            return print('✅ The password is valid.')

        print(check)
        return print(DASH_LINE)
        
        # We don't have to check for the raised exception beforehand
        # since we are handling all the possible errors in the __main__.py file.

    def check_config(self) -> bool:
        """The check config method to manipulate with the configuration file
        before the program opens the menu. It is useful when the user did not
        provide their credits to log in and this function exactly catches those
        moments.

        Returns:
            bool: The check result.
        """
        if not self.config:
            self.logger.warning('Hey, looks like you did not set up your configuration yet')
            choice = convert_choice(sinput('but would you want to (y/n)? '))
            if choice:  # Checking for the "True" case.
                self.setup()

                # The setup process was already finished.
                self.logger.info('You are ready to go, run the program again and explore the features.')
                return True  # At this point, the config will exist.

        return False

    def setup(self) -> NoReturn:
        """The setup method called by --setup flag.

        Returns:
            NoReturn: This means the method returns nothing.
        """
        self.logger.info('Setup process has been started.')
        name = sinput('What name you would like to set? ')
        password = sinput('What about password? ')

        with open(f'{PATH}/config.json', 'w') as fp:
            json.dump({'name': name, 'password': password}, fp=fp, indent=4)

        self.logger.info('Setup process was finished successfully.')
        self.logger.info(f'Current username: {name}')
        self.logger.info(f'Current password: {password}')

    def menu(self):
        """The main menu: should be called when the app gets no flags."""
        try:
            # Menu stuff.
            print(MENU_INFO)
            print(DASH_LINE)

            # Asking the user to choose one of the features.
            option = int(input('What option would you choose? '))
            return self.__dir__()[option - 1]()  # Consequently calling the method.

        except (ValueError, TypeError, IndexError) as e:
            self.logger.error(e)

    def show_data(self):
        """The data showing method to make the user able to visualize
        their data, i.e. accounts in a pretty-formatted table."""
        table = TabulateData()
        table.set_columns(['network', 'email', 'password'])

        results = self.database.push('SELECT * FROM passwords;').fetchall()
        table.set_rows(results)

        print(table.render())

    def export_data(self) -> str:
        """The data exporting method to make the user able to extract

        all of their data into the `passwords.txt` file."""
        path = sinput('Enter the path you would like to save your data in.\n'
                      'For example, Desktop/main: ')

        try:
            with open(f'{HOME_DIR}/{path}/passwords.txt', 'w') as f:
                f.write(self.show_data())

            self.logger.info('Exported all of your passwords successfully.')

        except FileNotFoundError as e:
            self.logger.error(f'Something went wrong: {e}')

    @staticmethod
    def _get_params(message: str, options: tuple) -> dict:
        """The interactive way to get kwargs that will be passed in `generate_password`.

        Args:
            message (str): A formattable message for all inputs.
            options (tuple): A tuple of options to provide.

        Returns:
            dict: A dictionary of necessary keys.
        """
        inputs = {option: sinput(message.format(option)) for option in options}
        print(DASH_LINE)
        return inputs

    @staticmethod
    def _true_false_only(message: str, options: tuple):
        """Does the same stuff as _get_params, but is limited in arguments choice.
        
        Here y | yes | + considered as True, anything else as False."""
        inputs = {option: convert_choice(sinput(message.format(option))) for option in options}
        print(DASH_LINE)
        return inputs

    @keep_living
    def generate_password(self, **kwargs) -> str:
        """This function is created to generate passwords of the given length."""
        global BASE, NUMBERS, UPPERCASE, SPECIAL
        options = ('numbers', 'uppercase', 'special characters')

        length = int(input('Enter the length: '))
        kwargs = kwargs or self._true_false_only('Enter the {} option: ', options)

        if kwargs.pop('numbers'):
            BASE += NUMBERS

        if kwargs.pop('uppercase'):
            BASE += UPPERCASE

        if kwargs.pop('special characters'):
            BASE += SPECIAL

        result = random.choices(BASE, k=length)
        print(''.join(result))

    @keep_living
    def save_password(self, **kwargs) -> str:
        """This function is created to save passwords according to the given credits."""
        options = ('network', 'email', 'content')
        kwargs = kwargs or self._get_params('Enter the {} credits: ', options)

        self.database.add(**kwargs)
        self.logger.info('✅ Inserted the data successfully.')

    def code_statistics(self) -> str:
        """See the code statistics of the application."""
        ctr = Counter()

        for ctr['files'], f in enumerate(glob('./**/*.py', recursive=True)):
            with open(f, encoding='UTF-8') as fp:
                for ctr['lines'], line in enumerate(fp, ctr['lines']):
                    line = line.lstrip()
                    ctr['classes'] += line.startswith('class')
                    ctr['functions'] += line.startswith('def')

        print('\n'.join(f'{k.capitalize()}: {v}' for k, v in ctr.items()))

    def check_owner(self) -> bool:
        """This is the method to check the correct owner beforehand.

        Raises:
            NotOwner: If the given credits did not match.

        Returns:
            bool: True, if the user passed the owner check.
        """
        self.logger.info('Login process has been started.')
        name = sinput('Enter your name: ')
        password = sinput('Enter your password: ')

        if name == self.config['name'] and password == self.config['password']:
            print(f'Welcome back, {name}!\n{DASH_LINE}')
            return True

        raise NotOwner
