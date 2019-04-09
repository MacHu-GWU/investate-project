# -*- coding: utf-8 -*-

from __future__ import division

try:
    from itertools import izip_longest as zip_longest
except:
    from itertools import zip_longest

from attrs_mate import attr, LazyClass

from .validators import Validators


class IncreasingMode(object):
    linear = "linear"
    compound = "compound"


@attr.s
class TimeSeries(object):
    """
    :param period_change: [0.1, 0.2, 0.3] means first period increase 10%,
        second period increase 20%, third period increase 30%
    """
    initial_value = attr.ib(validator=Validators.non_negative_number)
    period_change = attr.ib()
    mode = attr.ib(validator=attr.validators.in_((IncreasingMode.linear, IncreasingMode.compound)))
    length = attr.ib()

    OPT_INCREASING_MODE = IncreasingMode

    def init_period_change(self):
        if isinstance(self.period_change, (tuple, list)):
            yoy_change = list()
            for change, _ in zip_longest(self.period_change, range(self.length)):
                if change is None:
                    yoy_change.append(0)
                else:
                    yoy_change.append(change)
            self.period_change = yoy_change
        else:
            self.period_change = [self.period_change, ] * self.length

    def __attrs_post_init__(self):
        self.init_period_change()

    @LazyClass.lazyproperty
    def cum_change_array(self):
        """
        Cumulative change for every year. For example, if the cumulative change
        on 5th year is 1.3, then the value on 5th year is initial value * 1.3.
        """
        array = list()
        if self.mode == IncreasingMode.compound:
            v = 1
            for change in self.period_change:
                v = v * (1 + change)
                array.append(v)
        elif self.mode == IncreasingMode.linear:
            v = 0
            for change in self.period_change:
                v += change
                array.append(1.0 + v)
        return array

    @LazyClass.lazyproperty
    def value_array(self):
        return [self.initial_value * v for v in self.cum_change_array]

    @LazyClass.lazyproperty
    def avg_change_compound(self):
        return self.cum_change_array[-1] ** (1 / self.length) - 1

    @LazyClass.lazyproperty
    def avg_change_linear(self):
        return (self.cum_change_array[-1] - 1) / self.length


TS = TimeSeries


@attr.s
class HouseValueTS(TimeSeries):
    pass


@attr.s
class RentalTS(TimeSeries):
    pass
