from collections import namedtuple
from csv import reader


class FancyReader:
    _row_cls = None

    def __init__(self, r, fieldnames=None, *args, **kwargs):
        self.reader = reader(r, *args, **kwargs)
        self.fieldnames = fieldnames

    @property
    def Row(self):
        if self._row_cls is None:
            self._row_cls = namedtuple('Row', self.fieldnames)
        return self._row_cls

    @property
    def line_num(self):
        return self.reader.line_num

    def __iter__(self):
        return self

    def __next__(self):
        if self.fieldnames is None:
            self.fieldnames = next(self.reader)

        line = next(self.reader)
        return self.Row(*line)
