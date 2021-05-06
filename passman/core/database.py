import sqlite3
from typing import NoReturn, Optional

from .constants import PATH
from .logger import create_logger

__all__ = ('DatabaseManager',)


class DatabaseManager:
    """The Database Manager class to ease up database manipulation."""

    def __init__(self, path: str = f'{PATH}/passwords.db'):
        self._connection = sqlite3.connect(path)
        self.cursor = self._connection.cursor()
        self.logger = create_logger(self.__class__.__name__)

        self._build_schema()  # Simply, the setup process.

    def push(self, sql: str, args: tuple = None) -> NoReturn:
        if args:
            self.cursor.execute(sql, args)
        else:
            self.cursor.execute(sql)

        self._connection.commit()

    def _build_schema(self) -> NoReturn:
        """This is the method that simply does the setup process."""
        self.logger.info('Trying to build the schema...')

        try:
            with open(f'{PATH}/assets/schema.sql', 'r') as f:
                schema = f.read()

            self.push(schema)
            self.logger.info('Built the schema successfully.')

        except Exception as e:
            self.logger.error(f'Failed to build: {e}')

    def add(self, network: str, email: str, content: str) -> NoReturn:
        query = 'INSERT INTO passwords(network, email, content) VALUES(?, ?, ?);'

        try:
            self.push(query, (network, email, content))
        except sqlite3.IntegrityError:
            self.logger.error('This network credits already exist in the database.')

    def remove(self, network: str) -> NoReturn:
        query = 'DELETE FROM passwords WHERE network = ?;'
        self.push(query, network)

    def update(self, query: str, values: tuple) -> NoReturn:
        self.push(query, values)
