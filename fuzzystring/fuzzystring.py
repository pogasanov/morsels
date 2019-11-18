import unicodedata


class FuzzyString:
    def __init__(self, string):
        self.string = string
        self.converted = self._normalize_string(string)

    def _normalize_string(self, string):
        return self.NFD(self.NFD(string).casefold())

    def NFD(self, string):
        return unicodedata.normalize('NFD', string)

    def __str__(self):
        return str(self.string)

    def __repr__(self):
        return repr(self.string)

    def __eq__(self, other):
        return self.converted == self._normalize_string(other)

    def __lt__(self, other):
        return self.converted < other

    def __gt__(self, other):
        return self.converted > other

    def __le__(self, other):
        return self.converted <= other

    def __ge__(self, other):
        return self.converted >= other

    def __add__(self, other):
        return self.__class__(self.converted + other)

    def __contains__(self, item):
        return item.lower() in self.converted
