# -*- coding: utf-8 -*-

from __future__ import division
import attr
import six
import math
import pandas as pd
from constant2 import Constant
from attrs_mate import LazyClass

from .validators import Validators


@attr.s
class TermLoan(object):
    principal = attr.ib(validator=Validators.non_negative_number)
    rate_yearly = attr.ib(validator=Validators.percentage_validator)
    term_year = attr.ib(validator=Validators.year_validator)

    @LazyClass.lazyproperty
    def rate_monthly(self):
        return self.rate_yearly / 12

    @LazyClass.lazyproperty
    def term_month(self):
        return self.term_year * 12

    @LazyClass.lazyproperty
    def info(self):
        return "principal-{}-rate-{}-year-{}".format(
            self.principal, self.rate_yearly, self.term_year)


class AmortizationField(Constant):
    year = "year"
    month = "month"
    interest = "interest"
    principal = "principal"
    cum_interest = "cum_interest"
    cum_principal = "cum_principal"
    cum_payment = "cum_payment"
    principal_left = "principal_left"


AmoField = AmortizationField


class LoanPayment(object):
    amortization_money_columns = [
        AmoField.interest, AmoField.principal,
        AmoField.cum_interest, AmoField.principal, AmoField.cum_payment,
        AmoField.principal_left,
    ]
    amortization_columns = [AmoField.year, AmoField.month] + amortization_money_columns

    @property
    def amortization(self):
        raise NotImplementedError


@attr.s
class EqualLoanPayment(LoanPayment, TermLoan):
    """

    :param principal: number
    :param rate_yearly: number, 0 ~ 1
    :param term_year: number, 1 ~ 30

    **中文文档**

    等额本息月还款 = 贷款本金 x 月利率 x (1 ＋ 月利率) ^ 还款月数 / (((1 ＋ 月利率) ^ 还款月数) - 1)
    """

    @LazyClass.lazyproperty
    def monthly_payment(self):
        if self.principal > 0:
            if self.rate_monthly == 0:
                return self.principal / self.term_month
            else:
                return self.principal * self.rate_monthly \
                       * (1 + self.rate_monthly) ** self.term_month \
                       / ((1 + self.rate_monthly) ** self.term_month - 1)
        else:
            return 0

    @LazyClass.lazyproperty
    def amortization(self):
        """

        :return: ``pandas.DataFrame``
        """
        principal_left = self.principal
        monthly_payment = self.monthly_payment
        cum_payment_interest = 0
        cum_payment_principal = 0
        df = []
        for month in range(1, self.term_month + 1):
            year = math.ceil(month / 12)
            payment_interest = principal_left * self.rate_monthly
            payment_principal = monthly_payment - payment_interest
            cum_payment_interest += payment_interest
            cum_payment_principal += payment_principal
            cum_payment = cum_payment_interest + cum_payment_principal
            principal_left -= payment_principal
            df.append((
                year, month,
                round(payment_interest),
                round(payment_principal),
                round(cum_payment_interest),
                round(cum_payment_principal),
                round(cum_payment),
                round(principal_left),
            ))
        df = pd.DataFrame(df, columns=self.amortization_columns)
        df.index = df[AmoField.month]
        return df


@attr.s
class EqualPrincipalPayment(LoanPayment, TermLoan):
    """

    :param principal: number
    :param rate_yearly: number, 0 ~ 1
    :param term_year: number, 1 ~ 30

    **中文文档**

    等额本金月还款 = (贷款本金 / 还款月数) + (本金 — 已归还本金累计额) x 每月利率
    """

    @LazyClass.lazyproperty
    def amortization(self):
        """

        :return: ``pandas.DataFrame``
        """
        principal_left = self.principal
        monthly_payment_principal = self.principal / self.term_month
        cum_payment_interest = 0
        cum_payment_principal = 0
        df = []
        for month in range(1, self.term_month + 1):
            year = math.ceil(month / 12)
            payment_principal = monthly_payment_principal
            payment_interest = principal_left * self.rate_monthly
            cum_payment_interest += payment_interest
            cum_payment_principal += payment_principal
            cum_payment = cum_payment_interest + cum_payment_principal
            principal_left -= monthly_payment_principal
            df.append((
                year, month,
                round(payment_interest),
                round(payment_principal),
                round(cum_payment_interest),
                round(cum_payment_principal),
                round(cum_payment),
                round(principal_left),
            ))
        df = pd.DataFrame(df, columns=self.amortization_columns)
        df.index = df[AmoField.month]
        return df


def compare_amortization(payment_list):
    df = pd.DataFrame()
    for col in LoanPayment.amortization_columns:
        for payment in payment_list:
            df_amo = payment.amortization
            new_col = "{info}-{name}_{field}".format(
                info=payment.info,
                name=payment.__class__.__name__,
                field=col,
            )
            df[new_col] = df_amo[col]
    return df
