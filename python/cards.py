#!/usr/bin/env python
import collections
import functools
import operator
import random
import typing
import sys

# TODO: Introduce the typing module and allow (or enforce?) types associated
# with each field for use in type checking 
#import typing

def rcname():
    letters = list(map(lambda i: chr(ord('A') + i), range(26)))
    return ''.join(random.choice(letters) for _ in range(10))

def immutable(cls=None, fields=None):
    assert bool(cls is not None) ^ bool(fields is not None), \
        'Pass fields as kwarg or dont invoke decorator'

    def decorator(name, inner_fields, cls):
        name = cls.__name__
        print(inner_fields)
        field_names, field_types = zip(*map(lambda i: (lambda t: t+((None,)*(2-len(t))))(
            (i,) if type(i) not in (list, tuple) else tuple(i)), inner_fields))
        field_d = dict(zip(field_names, field_types))
        def make_c(self, *args, **kwargs):
            parg_i = iter(args)
            for fn in field_names:
                val = kwargs.get(fn, None) or next(parg_i)
                print("arg {} of class {} is type {}, should be {}".format(
                    val, name, type(val), field_d[fn]))

        ntc_type = type(name+'_nt', (collections.namedtuple(
            f"{name}Parent", tuple(field_names)),), {'__init__': make_c})
        cls_type = type(name, (cls, ntc_type), {})
        return cls_type

    n = rcname()
    return (functools.partial(decorator, n, fields) if fields else
            decorator(n, cls.__fields__, cls))

@immutable
class WinStat(object):
    __fields__ = [
        ('wins', int),
        ('loses', int),
        ('unfinished', int)
    ]

    @property
    def total(self):
        return self.wins + self.loses

    @property
    def win_ratio(self):
        return self.wins / float(self.total)

    def __add__(self, other):
        return self.__class__(self.wins + other.wins,
                              self.loses + other.loses,
                              self.unfinished + other.unfinished)

    def __iadd__(self, other):
        return self.__add__(other)

@immutable
class RecordItem(object):
    __fields__ = [
        ('won', bool)
    ]


@immutable
class StaticDeck(object):
    __fields__ = [
        ('cards', None),
        ('record', typing.List[RecordItem]),
    ]


@immutable
class Deck(object):
    __fields__ = (
        ("history", typing.List[StaticDeck]),
    )

    def joined_stats(self) -> WinStat:
        def record_stat(recor_items):
            wins = sum(r.won for r in recor_items)
            return WinStat(wins, len(recor_items) - wins, 0)

        return functools.reduce(operator.add, map(record_stat, map(
            operator.attrgetter('record'), self.history)))

def main(nver_cap, ngame_cap):
    d = Deck([
        StaticDeck("cards", [
            RecordItem(bool(random.randrange(2)))
            for _ in range(random.randrange(ngame_cap) + 1)])
        for __ in range(random.randrange(nver_cap) + 1)])
    s = d.joined_stats()
    print("Joined stats for new deck are:\n\t{} wins / {} games for {:.2f}%"
          .format(s.wins, s.total, 100*s.win_ratio))

if __name__ == '__main__':
    main(int(sys.argv[1]), int(sys.argv[2]))
