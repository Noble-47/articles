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

#    def __setattr__(self, name, value):
 #       cls = type(self)
  #      if len(name) == 1:
   #         if self._label is not None and name in self._label:
    #            err = f"readonly attribute {name}"
     #       elif name.islower():
      #          err = f"cannot set attribute 'a' to 'z' in {cls.__name__}"
       #     else:
        #        err = ""
         #   if err:
          #      raise AttributeError(err)
       # super().__setattr__(name, value)


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
