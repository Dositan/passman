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


class PasswordManager:
    """The Password Manager class to manipulate with generating passwords."""

    def __init__(self):
        self.logger = create_logger(self.__class__.__name__)
        self.database = DatabaseManager()
        self.strength = PasswordStrength()  # TODO: Use it somewhere.

        with open(f'{PATH}/config.json') as file:
            self.config = json.load(file)

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

    def menu(self) -> NoReturn:
        """The main menu: should be called when the app gets no flags.

        Returns:
            NoReturn: Means that the method returns nothing.
        """
        ways = (self.generate_password, self.save_password, self.show_data,
                self.export_data, self.code_statistics)

        try:
            # Menu stuff.
            print(MENU_INFO)
            print(DASH_LINE)

            option = int(input('What option would you choose? '))
            print(ways[option - 1]())

        except (ValueError, TypeError, IndexError) as e:
            self.logger.error(e)

    def show_data(self) -> str:
        """The data showing method to make the user able to visualize
        their data, i.e. accounts in a pretty-formatted table.

        Returns:
            str: The rendered table.
        """
        table = TabulateData()
        table.set_columns(['network', 'email', 'password'])

        results = self.database.push('SELECT * FROM passwords;').fetchall()
        table.set_rows(results)

        return table.render()

    def export_data(self) -> str:
        """The data exporting method to make the user able to extract

        all of their data into the `passwords.txt` file.

        Returns:
            str: The dashline to avoid 'None' caused by printing.
        """
        path = sinput('Enter the path you would like to save your data in.\n'
                      'For example, Desktop/main: ')

        try:
            with open(f'{HOME_DIR}/{path}/passwords.txt', 'w') as f:
                f.write(self.show_data())

            self.logger.info('Exported all of your passwords successfully.')

        except FileNotFoundError as e:
            self.logger.error(f'Something went wrong: {e}')

        return DASH_LINE  # Avoid 'None' caused by printing.

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

    def generate_password(self, **kwargs) -> str:
        """This function is created to generate passwords of the given length.

        Returns:
            str: The successfully-generated password.
        """
        global BASE, NUMBERS, UPPERCASE, SPECIAL
        options = ('length', 'numbers', 'uppercase', 'special characters')

        kwargs = kwargs or self._get_params('Enter the {} option: ', options)
        length = int(kwargs.pop('length', 20))

        if kwargs.pop('numbers'):
            BASE += NUMBERS

        if kwargs.pop('uppercase'):
            BASE += UPPERCASE

        if kwargs.pop('special characters'):
            BASE += SPECIAL

        result = random.choices(BASE, k=length)
        return ''.join(result)

    def save_password(self, **kwargs) -> str:
        """This function is created to save passwords according to the given credits.

        Returns:
            str: The successfully-saved password.
        """
        options = ('network', 'email', 'content')
        kwargs = kwargs or self._get_params('Enter the {} credits: ', options)

        self.database.add(**kwargs)
        self.logger.info('Inserted the data successfully.')
        return DASH_LINE  # Avoid 'None' caused by printing.

    def code_statistics(self) -> str:
        """See the code statistics of the application."""
        ctr = Counter()

        for ctr['files'], f in enumerate(glob('./**/*.py', recursive=True)):
            with open(f, encoding='UTF-8') as fp:
                for ctr['lines'], line in enumerate(fp, ctr['lines']):
                    line = line.lstrip()
                    ctr['classes'] += line.startswith('class')
                    ctr['functions'] += line.startswith('def')

        return '\n'.join(f'{k.capitalize()}: {v}' for k, v in ctr.items())

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
