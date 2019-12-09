class alias:
    def __init__(self, field, write=False):
        self.field = field
        self.write = write

    def __get__(self, instance, owner):
        return getattr(instance or owner, self.field)

    def __set__(self, instance, value):
        if not self.write:
            raise AttributeError
        setattr(instance, self.field, value)
