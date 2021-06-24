from typing import List, Tuple

__all__ = ('TabulateData',)


class TabulateData:
    def __init__(self):
        self._rows = []
        self._widths = []
        self._columns = []

    def set_columns(self, columns: List[str]):
        """Set columns for the visual table.

        Args:
            columns (List[str]): A list of strings (names) of columns.
        """
        self._columns = columns
        self._widths = [len(c) + 2 for c in columns]

    def _add_row(self, row: Tuple[str]):
        """Add a row for the visual table.

        Args:
            row (Tuple[str]): A tuple of values of columns.
        """
        rows = [str(r) for r in row]
        self._rows.append(rows)

        for index, element in enumerate(rows):
            width = len(element) + 2
            if width > self._widths[index]:
                self._widths[index] = width

    def set_rows(self, rows: List[Tuple[str]]):
        """Set multiple rows for the visual table.

        This just is an iterative way of the self._add_row method.

        Args:
            rows (List[Tuple[str]]): A list of tuples of values of columns.
        """
        for row in rows:
            self._add_row(row)

    def render(self) -> str:
        """The main method that puts all the magic together.

        This method visualizes the table manipulating with loads of values.

        Returns:
            str: The rendered table.
        """
        sep = '+'.join('-' * w for w in self._widths)
        sep = f'+{sep}+'

        to_draw = [sep]

        def get_entry(data: List[str]):
            elem = '|'.join(f'{e:^{self._widths[i]}}' for i, e in enumerate(data))
            return f'|{elem}|'

        to_draw.append(get_entry(self._columns))
        to_draw.append(sep)

        for row in self._rows:
            to_draw.append(get_entry(row))

        to_draw.append(sep)
        return '\n'.join(to_draw)
