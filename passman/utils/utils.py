import json
import random
from typing import NoReturn, Optional, Union

from passman.core import DatabaseManager, create_logger
from passman.core.constants import *
from passman.utils import NotOwner, TabulateData

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

        with open(f'{PATH}/config.json') as file:
            self.config = json.load(file)

    def setup(self) -> NoReturn:
        """The setup method called by --setup flag.

        Returns:
            NoReturn: This means the method returns nothing.
        """
        self.logger.info('Setup process has been started.')
        name = input('What name you would like to set? ')
        password = input('What about password? ')

        with open(f'{PATH}/config.json', 'w') as fp:
            json.dump({'name': name, 'password': password}, fp=fp, indent=4)

        self.logger.info('Setup process was finished successfully.')
        self.logger.info(f'Current username: {name}')
        self.logger.info(f'Current password: {password}')

    def menu(self) -> NoReturn:
        # Should be called when the app got no flags.
        ways = (self.generate_password, self.save_password, self.show_data,
                self.export_data)

        try:
            # Menu stuff.
            print(MENU_INFO)
            print('-' * DASH_TIMES)

            option = int(input('What option would you choose? '))
            print(ways[option - 1]())

        except (ValueError, TypeError, IndexError) as e:
            self.logger.error(e)

    def show_data(self):
        table = TabulateData()
        table.set_columns(('network', 'email', 'password'))

        query = 'SELECT * FROM passwords;'
        results = self.database.cursor.execute(query).fetchall()
        table.set_rows(results)

        return table.render()

    def export_data(self):
        path = sinput('Enter the path you would like to save your data in.\n'
                      'For example, Desktop/main: ')

        try:
            with open(f'{HOME_DIR}/{path}/passwords.txt', 'w') as f:
                f.write(self.show_data())

            self.logger.info('Exported all of your passwords successfully.')

        except FileNotFoundError as e:
            self.logger.error(f'Something went wrong: {e}')

        return '-' * DASH_TIMES  # Avoid 'None' caused by printing.

    @staticmethod
    def _get_params(message: str, options: tuple):
        """The interactive way to get kwargs that will be passed in `generate_password`.

        Args:
            message (str): A formattable message for all inputs.
            options (tuple): A tuple of options to provide.

        Returns:
            dict: A dictionary of necessary keys.
        """
        inputs = {option: sinput(message.format(option)) for option in options}
        print('-' * DASH_TIMES)
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

    def save_password(self, **kwargs) -> NoReturn:
        """This function is created to save passwords according to the given credits.

        Returns:
            str: The successfully-saved password.
        """
        options = ('network', 'email', 'content')
        kwargs = kwargs or self._get_params('Enter the {} credits: ', options)

        self.database.add(**kwargs)
        self.logger.info('Inserted the data successfully.')
        return '-' * DASH_TIMES  # Avoid 'None' caused by printing.

    def check_owner(self):
        """This is the method to check the correct owner beforehand."""
        self.logger.info('Login process has been started.')
        name = sinput('Enter your name: ')
        password = sinput('Enter your password: ')
        # name and password must match with the data in
        # config.json, so if it matches we can continue the process.

        if name == self.config['name'] and password == self.config['password']:
            print(f'Welcome back, {name}!\n' + '-' * DASH_TIMES)
            return True

        raise NotOwner
