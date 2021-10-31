from typing import List, Tuple

from passman import config


def compare_data(login: str, password: str) -> bool:
    """Used in comparing input details with config data.

    Parameters
    ----------
    login : str
        login credits written in config.json
    password : str
        password credits writte in config.json

    Returns
    -------
    bool
        True if credits match, False in any other cases.
    """
    if login == config["name"] and password == config["password"]:
        return True
    return False


class TabulateData:
    def __init__(self):
        self._rows = []
        self._widths = []
        self._columns = []

    def set_columns(self, columns: List[str]) -> None:
        """Set columns for the visual table.

        Parameters
        ----------
        columns : List[str]
            A list of strings (names) of columns.
        """
        self._columns = columns
        self._widths = [len(c) + 2 for c in columns]

    def _add_row(self, row: Tuple[str]) -> None:
        """Add a row for the visual table.

        Parameters
        ----------
        row : Tuple[str]
            A tuple of values of columns.
        """
        rows = [str(r) for r in row]
        self._rows.append(rows)

        for index, element in enumerate(rows):
            width = len(element) + 2
            if width > self._widths[index]:
                self._widths[index] = width

    def set_rows(self, rows: List[Tuple[str]]) -> None:
        """Set multiple rows for the visual table at once.

        This just is an iterative way of the `_add_row` method.

        Parameters
        ----------
        rows : List[Tuple[str]]
            A list of tuples of values of columns.
        """
        for row in rows:
            self._add_row(row)

    def render(self) -> str:
        """This puts all the magic together.

        This method visualizes the table manipulating with loads of values.

        Returns
        -------
        str
            The rendered table.
        """
        sep = "+".join("-" * w for w in self._widths)
        sep = f"+{sep}+"

        to_draw = [sep]

        def get_entry(data: List[str]):
            elem = "|".join(f"{e:^{self._widths[i]}}" for i, e in enumerate(data))
            return f"|{elem}|"

        to_draw.append(get_entry(self._columns))
        to_draw.append(sep)

        for row in self._rows:
            to_draw.append(get_entry(row))

        to_draw.append(sep)
        return "\n".join(to_draw)
