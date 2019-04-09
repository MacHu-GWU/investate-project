# -*- coding: utf-8 -*-

from __future__ import print_function
from tabulate import tabulate


def pprint_df(df):
    """
    Pretty print dataframe in fancy grid ascii table.

    :param df: ``pandas.DataFrame``
    """
    t = tabulate(df, headers=df.columns, showindex="always", tablefmt="fancy_grid")
    print(t)
