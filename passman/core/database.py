import sqlite3
from typing import NoReturn

from .constants import PATH
from .logger import create_logger

__all__ = ('DatabaseManager',)


class DatabaseManager:
    """The Database Manager class to ease up database manipulation."""

    def __init__(self, path: str = f'{PATH}/passwords.db'):
        self._connection = sqlite3.connect(path)
        self.cursor = self._connection.cursor()
        self.logger = create_logger(self.__class__.__name__)

        check = self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='passwords';").fetchone()
        if not check:
            self.logger.exception('Could not find the table.')
            self._build_schema()  # Simply, the setup process.
            # Build the schema only if the file does not exist yet.

    def push(self, sql: str, args: tuple = None):
        """The push method to ease up the database manipulation for the developer.

        Args:
            sql (str): An SQL query to execute.
            args (tuple, optional): A tuple of arguments to pass in. Defaults to None.
        """
        if args:
            data = self.cursor.execute(sql, args)
            if sql.lower().startswith('select'):  # no commit() is needed.
                return data

            return self._connection.commit()

        return self.cursor.execute(sql)

    def _build_schema(self) -> NoReturn:
        """This is a method that simply runs the database setup process.

        Returns:
            NoReturn: Means that the method returns nothing.
        """
        self.logger.info('Trying to build the schema...')

        try:
            with open(f'{PATH}/assets/schema.sql', 'r') as f:
                schema = f.read()

            self.push(schema)
            self.logger.info('Built the schema successfully.')

        except Exception as e:
            self.logger.error(f'Failed to build: {e}')

    def add(self, network: str, email: str, content: str) -> NoReturn:
        """A quick add method that saves the account
        data according to the given parameters.

        Args:
            network (str): The network name.
            email (str): The email address for the network.
            content (str): The password for the network you log in with.

        Returns:
            NoReturn: Means that the method returns nothing.
        """
        query = 'INSERT INTO passwords(network, email, content) VALUES(?, ?, ?);'

        try:
            self.push(query, (network, email, content))
        except sqlite3.IntegrityError:
            self.logger.error('This network credits already exist in the database.')

    def remove(self, network: str) -> NoReturn:
        """A quick remove method that deletes a row with the given network
        from the local database.

        Args:
            network (str): The network name, case matters.

        Returns:
            NoReturn: Means that the method returns nothing.
        """
        query = 'DELETE FROM passwords WHERE network = ?;'
        self.push(query, network)

    def update(self, query: str, values: tuple) -> NoReturn:
        """A quick update method that runs the given query using given values.

        Args:
            query (str): An SQL query to execute.
            values (tuple): A tuple of values to replace the old values with.

        Returns:
            NoReturn: Means that the method returns nothing.
        """
        self.push(query, values)
