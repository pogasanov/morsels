class Vector:
    __slots__ = ['x', 'y', 'z']

    def __init__(self, x, y, z):
        super().__setattr__('x', x)
        super().__setattr__('y', y)
        super().__setattr__('z', z)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __iter__(self):
        return (i for i in (self.x, self.y, self.z))

    def __add__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError
        return self.__class__(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError
        return self.__class__(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        if not isinstance(other, int):
            raise TypeError
        return self.__class__(self.x * other, self.y * other, self.z * other)

    def __rmul__(self, other):
        if not isinstance(other, int):
            raise TypeError
        return self.__class__(self.x * other, self.y * other, self.z * other)

    def __truediv__(self, other):
        if not isinstance(other, int):
            raise TypeError
        return self.__class__(self.x / other, self.y / other, self.z / other)

    def __setattr__(self, name, value):
        raise AttributeError()
