#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from pytest import raises, approx
from investate.timeseries import TS


class TestTimeSeries(object):
    def test_init(self):
        ts = TS(initial_value=0, period_change=0.1, mode=TS.OPT_INCREASING_MODE.compound, length=30)
        assert ts.period_change == [0.1, ] * 30

        ts = TS(initial_value=0,
                period_change=[0.1, None, 0.3, None, 0.5],
                mode=TS.OPT_INCREASING_MODE.compound, length=30)
        assert ts.period_change[:7] == [0.1, 0, 0.3, 0, 0.5, 0, 0]

    def test_cum_change_array(self):
        ts = TS(initial_value=0, period_change=1, mode=TS.OPT_INCREASING_MODE.compound, length=3)
        assert ts.cum_change_array == [2, 4, 8]

        ts = TS(initial_value=0, period_change=1, mode=TS.OPT_INCREASING_MODE.linear, length=3)
        assert ts.cum_change_array == [2, 3, 4]

        ts = TS(initial_value=0, period_change=0, mode=TS.OPT_INCREASING_MODE.compound, length=3)
        assert ts.cum_change_array == [1, 1, 1]

        ts = TS(initial_value=0, period_change=0, mode=TS.OPT_INCREASING_MODE.linear, length=3)
        assert ts.cum_change_array == [1, 1, 1]

    def test_value_array(self):
        ts = TS(initial_value=100, period_change=1, mode=TS.OPT_INCREASING_MODE.compound, length=3)
        assert ts.value_array == [200, 400, 800]

        ts = TS(initial_value=100, period_change=1, mode=TS.OPT_INCREASING_MODE.linear, length=3)
        assert ts.value_array == [200, 300, 400]

    def test_yearly_yield_compound(self):
        ts = TS(initial_value=0, period_change=1, mode=TS.OPT_INCREASING_MODE.compound, length=3)
        assert ts.avg_change_compound == approx(1.0)
        assert ts.avg_change_linear == approx(7.0 / 3)

        ts = TS(initial_value=0, period_change=1, mode=TS.OPT_INCREASING_MODE.linear, length=3)
        assert ts.avg_change_compound == (4 ** (1.0 / 3) - 1)
        assert ts.avg_change_linear == approx(1.0)


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
