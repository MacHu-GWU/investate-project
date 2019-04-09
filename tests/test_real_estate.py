# -*- coding: utf-8 -*-

import pytest
from pytest import raises, approx
from investate.real_estate import RealEstate, TimeSeries


class TestRealEstate(object):
    e1 = RealEstate(
        identifier="DC White House",
        buy_price=400000,
        down_perc=0.25,
        interests_rate_every_year=[2.875, ] * 5 + [3.875 * 5] + [4.875 * 20],
        mortgage_term_years=30,
        loan_payment_type=RealEstate.OPT_LOAN_PAYMENT_TYPE.EqualLoanPayment,

        house_value_initial=400000,
        house_value_yearly_change=0.025,
        house_value_changing_type=RealEstate.OPT_INCREASING_MODE.compound,

        rental_value_initial=2200,
        rental_value_yearly_change=0.025,
        rental_value_changing_type=RealEstate.OPT_INCREASING_MODE.compound,
        rental_months_per_year=11,

        cost_hoa_fee_each_month=115,
        cost_other_each_year=1200,
        cost_yearly_change=0.025,

        cost_home_insurance_perc_each_year=0.15 / 100,
        cost_property_tax_perc_each_year=0.01,
        mortgage_interests_tax_exempt_perc=0.2,
        mortgage_interests_tax_exempt_yearly_cap=750000,
    )

    print(e1.cash_flow)


# if __name__ == "__main__":
#     import os
#
#     basename = os.path.basename(__file__)
#     pytest.main([basename, "-s", "--tb=native"])
