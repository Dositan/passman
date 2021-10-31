# TODO: rewrite the whole logic using psycopg2
import logging
import sqlite3
from typing import Any

__all__ = ("DatabaseManager",)
log = logging.getLogger("passman.database")


class DatabaseManager:
    """The Database Manager class to ease up database manipulation."""

    def __init__(self):
        self._connection = sqlite3.connect("./data/passwords.db")
        self.cursor = self._connection.cursor()

        query = (
            "SELECT name FROM sqlite_master WHERE type='table' AND name='passwords';"
        )
        if (self.cursor.execute(query).fetchone()) is None:
            log.exception("Could not find the table.")
            self._build_schema()  # Simply, the setup process.
            # Build the schema only if the file does not exist yet.

    @property
    def connection(self) -> sqlite3.Connection:
        return self._connection

    def push(self, sql: str, args: tuple = ()) -> Any:
        """Push method to ease up the database manipulation for the developer.

        Parameters
        ----------
        sql : str
            An SQL query to execute.
        args : tuple, optional
            A tuple of arguments to pass in, by default None

        Returns
        -------
        Any
            SQL execution may return literally any type.
        """
        if args:
            data = self.cursor.execute(sql, args)
            if sql.lower().startswith("select"):  # no commit() is needed.
                return data

            return self._connection.commit()

        return self.cursor.execute(sql)

    def _build_schema(self) -> None:
        """This simply runs the database setup process."""
        log.info("Trying to build the schema...")

        with open("./data/build.sql", "r") as fp:
            schema = fp.read()
        try:
            self.push(schema)
            log.info("Built the schema successfully.")
        except Exception as e:
            log.error("Failed to build", exc_info=e)

    def add(self, network: str, email: str, content: str) -> None:
        """This saves an account data according to the given parameters.

        Parameters
        ----------
        network : str
            The network name.
        email : str
            The email address of the network.
        content : str
            The password of the network you log in with.
        """
        query = "INSERT INTO passwords(network, email, content) VALUES(?, ?, ?);"

        try:
            self.push(query, (network, email, content))
        except sqlite3.IntegrityError:
            log.error("This network credits already exist in the database.")

    def remove(self, _id: int) -> None:
        """This deletes a row with the given id.

        Parameters
        ----------
        _id : int
            The id of the user.
        """
        self.push("DELETE FROM passwords WHERE id = ?;", _id)
