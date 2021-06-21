import logging
import sqlite3

__all__ = ('DatabaseManager',)
log = logging.getLogger('passman.database')


class DatabaseManager:
    """The Database Manager class to ease up database manipulation."""

    def __init__(self):
        self._connection = sqlite3.connect('./passman/data/passwords.db')
        self.cursor = self._connection.cursor()

        table_exists = self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='passwords';").fetchone()
        if table_exists is None:
            log.exception('Could not find the table.')
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

    def _build_schema(self) -> None:
        """This is a method that simply runs the database setup process."""
        log.info('Trying to build the schema...')

        try:
            schema = '''
            CREATE TABLE IF NOT EXISTS passwords (
                network VARCHAR(20) PRIMARY KEY,
                email VARCHAR(100),
                content VARCHAR(50)
            );
            '''
            self.push(schema)
            log.info('Built the schema successfully.')

        except Exception as e:
            log.error(f'Failed to build: {e}')

    def add(self, network: str, email: str, content: str) -> None:
        """A quick add method that saves the account
        data according to the given parameters.

        Args:
            network (str): The network name.
            email (str): The email address for the network.
            content (str): The password for the network you log in with.
        """
        query = 'INSERT INTO passwords(network, email, content) VALUES(?, ?, ?);'

        try:
            self.push(query, (network, email, content))
        except sqlite3.IntegrityError:
            log.error('This network credits already exist in the database.')

    def remove(self, network: str) -> None:
        """A quick remove method that deletes a row with the given network
        from the local database.

        Args:
            network (str): The network name, case matters.
        """
        query = 'DELETE FROM passwords WHERE network = ?;'
        self.push(query, network)

    def update(self, query: str, values: tuple) -> None:
        """A quick update method that runs the given query using given values.

        Args:
            query (str): An SQL query to execute.
            values (tuple): A tuple of values to replace the old values with.
        """
        self.push(query, values)
