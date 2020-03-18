from collections import UserList
from itertools import cycle


class CyclicList(UserList):
    def __iter__(self):
        return cycle(self.data)

    def __getitem__(self, index):
        if isinstance(index, slice):
            start = index.start or 0
            stop = index.stop or (len(self.data) if start >= 0 else 0)
            return [
                self[i]
                for i in range(start, stop)
            ]
        return super().__getitem__(index % len(self))

    def __setitem__(self, key, value):
        key = key % len(self.data)
        return super().__setitem__(key, value)
