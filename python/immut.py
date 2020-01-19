#!/usr/bin/env python
import collections
import functools
import typing

class SetAny(object): pass

class ImmutOne(collections.namedtuple("ImmutOne", ("a", "b"))):
    def mul_baby(self):
        return self.a * self.b

class MetaImmut(type):
    __slots__ = []

def immutable(cls=None, fields=None):
    assert bool(cls is not None) ^ bool(fields is not None), \
        'Pass fields as kwarg or dont invoke decorator'

    def decorator(name, inner_fields, cls):
        return type(name, (collections.namedtuple(
            f"{name}Parent", tuple(inner_fields)), cls), {})

    return (functools.partial(decorator, "N1", fields) if fields else
            decorator("N1", cls.__fields__, cls))

@immutable
class ImmutThree(object):
    __fields__ = ['a', 'b']
    def mul_baby(self): self.a + self.b

@immutable(fields=['a', 'b'])
class ImmutFour(object):
    def mul_baby(self): self.a + self.b

class ImmutTwo(metaclass=MetaImmut):
    def __init__(self, a, b):
        self.a = a
        self.b = b

class ImmutFive(typing.NamedTuple):
    a: int
    b: int

    def mul_baby(self):
        return  self.a + self.b

def test_class(cls, cls_name):
    obj = cls(1, 2)
    print(f"Testing class ${cls_name}")
    print(f"obj a {obj.a} and b {obj.b}")

    try:
        print(f"obj slots ${obj.__slots__}")
    except:
        pass
    try:
        obj.a = 4
        print("Allowed obj.a = 4, FAILUE")
    except:
        print("Correct exception thrown on obj.a = 4")
        print(f"mul_baby ${obj.mul_baby()}")


test_class(ImmutOne, "ImmutOne")
test_class(ImmutTwo, "ImmutTwo")
test_class(ImmutThree, "ImmutThree")
test_class(ImmutFour, "ImmutFour")
test_class(ImmutFive, "ImmutFive")
