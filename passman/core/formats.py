
class TabulateData:
    def __init__(self):
        self._rows = []
        self._widths = []
        self._columns = []

    def set_columns(self, columns: tuple):
        self._columns = columns
        self._widths = [len(c) + 2 for c in columns]

    def _add_row(self, row: tuple):
        rows = [str(r) for r in row]
        self._rows.append(rows)

        for index, element in enumerate(rows):
            width = len(element) + 2
            if width > self._widths[index]:
                self._widths[index] = width

    def set_rows(self, rows: list):
        for row in rows:
            self._add_row(row)

    def render(self):
        sep = '+'.join('-' * w for w in self._widths)
        sep = f'+{sep}+'

        to_draw = [sep]

        def get_entry(data: list):
            elem = '|'.join(f'{e:^{self._widths[i]}}' for i, e in enumerate(data))
            return f'|{elem}|'

        to_draw.append(get_entry(self._columns))
        to_draw.append(sep)

        for row in self._rows:
            to_draw.append(get_entry(row))

        to_draw.append(sep)
        return '\n'.join(to_draw)
