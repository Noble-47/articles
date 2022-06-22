from numbers import Integral
import itertools


class Mysterious:
    def __add__(self, other):
        other_cls = type(other)
        return other_cls((5 + x for x in other), label=other._label)

    def __radd__(self, other):
        return self + other


class Point:
    def __init__(self, coordinates, label=None):
        self._coordinates = tuple(coordinates)
        self._label = label

    def __repr__(self):
        return f"Point([{','.join(str(x) for x in self._coordinates)}])"

    def __iter__(self):
        #       return PointIterator(self._coordinates)
        #       return iter(self._coordinates)
        return (x for x in self._coordinates)

    def __getitem__(self, index):
        cls = type(self)
        if isinstance(index, slice):
            return cls(self._coordinates[index])
        if isinstance(index, int):
            return self._coordinates[index]
        raise TypeError(
            f"{cls.__name__} indices must be integers or slices, not {type(index).__name__}"
        )

    def __getattr__(self, name):
        cls = type(self)
        msg = f"{cls.__name__} object has not attribute {name}"
        if self._label is None:
            raise AttributeError(msg)
        if len(name) == 1:
            l = self._label.find(name)
            if 0 <= l < len(self._coordinates):
                return self._coordinates[l]
        raise AttributeError(msg)

    def __setattr__(self, name, value):
        cls = type(self)
        if len(name) == 1:
            if self._label is not None and name in self._label:
                err = f"readonly attribute {name}"
            elif name.islower():
                err = f"cannot set attribute 'a' to 'z' in {cls.__name__}"
            else:
                err = ""
            if err:
                raise AttributeError(err)
        super().__setattr__(name, value)

    def __len__(self):
        return len(self._coordinates)

    def __add__(self, other):
        # goose typing : Look Before You Leap
        # allows only instances of class
        # would be a problem if some other class knows how to add a vector class
        # python first tries __add__ then __radd__
        # should raise a TypeError
        if isinstance(other, Point):
            label = (
                self._label
                if (other._label is None or len(other) < len(self))
                else other._label
            )
            return Point(
                a + b for a, b in itertools.zip_longest(self, other, fillvalue=0)
            )
        else:
            return NotImplemented
        # Duck typing
        # label = None
        # if not isinstance(other, Point):
        #     try:
        #         iter(other)
        #     except:
        #         return NotImplemented
        #     else:
        #         if not all(isinstance(i, Integral) for i in other):
        #             return NotImplemented
        #     if len(other) > len(self):
        #         raise Exception(
        #             f"{type(other).__name__} object must be of equal length with Point object"
        #         )
        #     label = self._label
        # if label is None:
        #     label = (
        #         self._label
        #         if (other._label is None or len(other) < len(self))
        #         else other._label
        #     )
        # return Point(
        #     (a + b for a, b in itertools.zip_longest(self, other, fillvalue=0)),
        #     label=label,
        # )

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        try:
            label = (
                self._label
                if (other._label is None or len(other) < len(self))
                else other._label
            )
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

    def __abs__(self):
        return math.sqrt(sum(x**2 for x in self))

    def __complex__(self):
        try:
            x, y = self._label[0], self._label[1]
            return complex(self.x, self.y)
        except:
            raise Exception(
                "Point instance must have at least two coordinates to be converted to complex form"
            )

    def __mul__(self, n: int):
        # scalar multiplication
        if isinstance(n, Integral):
            return Point(n * x for x in self)
        return NotImplemented

    def __rmul__(self, n):
        return self * n

    def __matmul__(self, other):
        # In Python.__version__ >= 3.5
        # the @ operator calls this method
        # A naive implementation of
        # dot product of points
        try:
            return sum(a * b for a, b in zip(self, other))
        except:
            return NotImplemented

    def __rmatmul__(self, other):
        # for Python.__version__ >= 3.5
        return self @ other


class PointIterator:
    def __init__(self, coordinates):
        self.coordinates = coordinates
        self.count = 0

    def __iter__(self):
        self.count = 0
        return self

    def __next__(self):
        if self.count >= len(self.coordinates):
            raise StopIteration
        value = self.coordinates[self.count]
        self.count += 1
        return value
