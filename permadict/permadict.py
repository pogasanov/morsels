from typing import Dict


class PermaDict(Dict):
    def __init__(self, *args, silent=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.silent = silent

    def __setitem__(self, key, value):
        try:
            self.__getitem__(key)
        except KeyError:
            super().__setitem__(key, value)
        else:
            if not self.silent:
                raise KeyError

    def update(self, __m=None, force=False, **kwargs):
        set_operation = self.force_set if force else self.__setitem__

        if __m:
            items = __m.items() if isinstance(__m, dict) else __m
            for key, value in items:
                set_operation(key, value)

        for key, value in kwargs.items():
            set_operation(key, value)

    def force_set(self, key, value):
        super().__setitem__(key, value)
