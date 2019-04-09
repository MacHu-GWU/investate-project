# -*- coding: utf-8 -*-

import pytest
from pytest import raises, approx
from investate.debug_tool import pprint_df
from investate.loan import AmoField, EqualLoanPayment, EqualPrincipalPayment


class TestEqualLoanPayment(object):
    def test_zero_principal(self):
        l = EqualLoanPayment(principal=0, rate_yearly=0, term_year=30)
        df_amo = l.amortization
        assert (df_amo[EqualLoanPayment.amortization_money_columns] == 0).all(axis=None)

        l = EqualPrincipalPayment(principal=0, rate_yearly=0, term_year=30)
        df_amo = l.amortization
        assert (df_amo[EqualPrincipalPayment.amortization_money_columns] == 0).all(axis=None)

    def test_zero_rate(self):
        l = EqualLoanPayment(principal=300000, rate_yearly=0, term_year=30)
        df_amo = l.amortization
        assert (df_amo[[AmoField.interest, AmoField.cum_interest]] == 0).all(axis=None)


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
