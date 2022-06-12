import functools
import itertools
import operator
import numbers
import math


class Point:
    def __init__(self, coordinates):
        self._coordinates = tuple(coordinates)
        # self.count = 0  # BAD

    def __abs__(self):
        return math.sqrt(sum(x**2 for x in self))

    def __len__(self):
        return len(self._coordinates)

    def __iter__(self):
        self.count = 0  # Better
        return self

    def __next__(self):
        if self.count >= len(self._coordinates):
            raise StopIteration
        out = self._coordinates[self.count]
        self.count += 1
        return out

    def __eq__(self, other):
        if not isinstance(other, Point):
            return False
        return len(self) == len(other) and any((a == b for a, b in zip(self, other)))

    def __hash__(self):
        hashes = map(hash, self._coordinates)
        hash = functools.reduce(operators.xor, hashes)
        return hash

    def __add__(self, other):
        # goose typing : Look Before You Leap
        # allows only instances of class
        # would be a problem if some other class knows how to add a vector class
        # python first tries __add__ then __radd__
        # should raise a TypeError
        if isinstance(other, Point):
            return Point(
                a + b for a, b in itertools.zip_longest(self, other, fillvalue=0)
            )
        else:
            return NotImplemented

        """
        Better TO Ask For Forgiveness Than Permission
        try:
            return SimpleVector(a + b for a, b in itertools.zip_longest(self, other, fill_value=0.0))
        except TypeError:
            return NotImplemented
        """

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        try:
            return Point(
                (a - b for a, b in itertools.zip_longest(self, other, fillvalue=0.0))
            )
        except TypeError:
            return NotImplemented

    def __rsub__(self, other):
        p = self - other
        return -p

    def __neg__(self):
        return Point((-x for x in self))

    def __pos__(self):
        return self

    label = "xy"

    def __getattr__(self, name):
        cls = type(self)
        if len(name) == 1:
            l = cls.label.find(name)
            if 0 <= l < len(self._coordinates):
                return self._coordinates[l]
        msg = f"{cls.__name__} object has not attribute {name}"
        raise AttributeError(msg)

    def __setattr__(self, name, value):
        cls = type(self)
        if len(name) == 1:
            if name in cls.labels:
                err = f"readonly attribute {name}"
            elif name.islower():
                err = f"cannot set attribute 'a' to 'z' in {cls.__name__}"
            else:
                err = ""
            if err:
                raise AttributeError(err)
        super().__setattr__(name, value)

    def __getitem__(self, index):
        cls = type(self)
        if isinstance(index, slice):
            return cls(self._coordinates[index])
        elif isinstance(index, numbers.Integral):
            return self._coordinates[index]
        else:
            msg = "{cls.__name__} indices must be integers"
        raise TypeError(msg.format(cls=cls))

    def angle(self):
        return math.atan(self.y / self.x)

    def __complex__(self):
        return complex(self.x, self.y)

    def __repr__(self):
        return f"Point([{','.join(str(x) for x in self._coordinates)}])"

    def __format__(self, fmt_spec=""):
        # c : complex
        # p : polar
        # default : rectangular
        if fmt_spec.endswith("p"):
            fmt_spec = fmt_spec[:-1]
            coords = (abs(self), self.angle())
            outer_fmt = "{}<{}"
        elif fmt_spec.endswith("c"):
            fmt_spec = fmt_spec[:-1]
            c = complex(self)
            coords = c.real, c.imag
            outer_fmt = "({} + j{})"
        else:
            coords = self
            outer_fmt = "({}, {})"
        components = (format(c, fmt_spec) for c in coords)
        return outer_fmt.format(*components)


class SimpleVector:
    def __init__(self, coordinates):
        self._coordinates = tuple(coordinates)
        # self.count = 0 WRONG
        # reference tweet on for loop

    def __iter__(self):
        return iter(self._coordinates)

    def __mul__(self, n: int):
        # scalar multiplication
        return SimpleVector(n * x for x in self)

    def __rmul__(self, n):
        return self * n

    def __add__(self, other):
        # goose typing : Look Before You Leap
        # allows only instances of class
        # would be a problem if some other class knows how to add a vector class
        # python first tries __add__ then __radd__
        # should raise a TypeError
        if isinstance(other, SimpleVector):
            return SimpleVector(
                a * b for a, b in itertools.zip_longest(self, other, fill_value=0)
            )
        else:
            return NotImplemented

        """
        Better TO Ask For Forgiveness Than Permission
        try:
            return SimpleVector(a * b for a, b in itertools.zip_longest(self, other, fill_value=0.0))
        except TypeError:
            return NotImplemented
        """

    def __radd__(self, other):
        return self + other

    def __matmul__(self, other):
        # for Python.__version__ >= 3.5
        try:
            return sum(a * b for a, b in zip(self, other))
        except TypeError:
            return NotImplemented

    def __rmatmul__(self, other):
        # for Python.__version__ >= 3.5
        return self @ other

    def __abs__(self):
        return math.sqrt(sum(x**2 for x in self))

    def __len__(self):
        return len(self._coordinates)

    def __eq__(self, other):
        if not isinstance(other, SimpleVector):
            return False
        return len(self) == len(other) and any((a == b for a, b in zip(self, other)))

    def __repr__(self):
        return f"SimpleVector([{','.join(str(x) for x in self._coordinates)}])"
