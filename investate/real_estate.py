# -*- coding: utf-8 -*-

from __future__ import print_function
from attrs_mate import attr, AttrsClass, LazyClass
from .loan import EqualLoanPayment, EqualPrincipalPayment
from .timeseries import TimeSeries, HouseValueTS, RentalTS

class MortgageType(object):
    term = "term"
    arm = "arm"


@attr.s
class RealEstate(AttrsClass):
    """

    :param cost_hoa_fee_each_month:
    :param cost_home_insurance_perc_each_year: ``cost_home_insurance_perc_each_year
        = home_insurance_per_year / house_value_on_that_year``
    :param cost_other_each_year: repair, maintenance cost.

    """
    identifier = attr.ib()
    buy_price = attr.ib()
    observation_years = attr.ib()

    # mortgage
    down_perc = attr.ib()


    interests_rate_every_year = attr.ib()
    mortgage_term_years = attr.ib()

    # house value time series
    house_value_initial = attr.ib()
    house_value_yearly_change = attr.ib()
    house_value_changing_type = attr.ib()

    # rental value time series
    rental_value_initial = attr.ib()
    rental_value_yearly_change = attr.ib()
    rental_value_changing_type = attr.ib()
    rental_months_per_year = attr.ib()

    loan_payment_type = attr.ib(
        validator=attr.validators.in_(
            (EqualLoanPayment, EqualPrincipalPayment)
        )
    )

    cost_hoa_fee_each_month = attr.ib()
    cost_other_each_year = attr.ib()
    cost_yearly_change = attr.ib() # yearly increment of hoa fee and other cost

    cost_home_insurance_perc_each_year = attr.ib()
    cost_property_tax_perc_each_year = attr.ib()

    mortgage_interests_tax_exempt_perc = attr.ib()
    mortgage_interests_tax_exempt_yearly_cap = attr.ib()

    OPT_INCREASING_MODE = TimeSeries.OPT_INCREASING_MODE

    class OPT_LOAN_PAYMENT_TYPE(object):
        EqualLoanPayment = EqualLoanPayment
        EqualPrincipalPayment = EqualPrincipalPayment

    @LazyClass.lazyproperty
    def down_payment(self):
        return self.buy_price * self.down_perc

    @LazyClass.lazyproperty
    def loan_perc(self):
        return 1 - self.down_perc

    @LazyClass.lazyproperty
    def loan_amount(self):
        return self.buy_price * self.loan_perc

    @LazyClass.lazyproperty
    def interest_rate_monthly(self):
        return self.interest_rate_yearly / 12

    # @LazyClass.lazyproperty
    # def loan(self):
    #     if self.
    #
    @LazyClass.lazyproperty
    def cashflow(self):
        df = list()
        for month in range(self.observation_years * 12):
            monthly_mortgage_payment_interest =
