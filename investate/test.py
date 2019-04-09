principal = 300000
interest_yearly = 0.02875
interest_monthly = interest_yearly / 12
term_years = 30
term_months = term_years * 12

monthly_payment = principal


def pmt(principal, interest_month, term_months):
    return principal * interest_month * (1 + interest_month) ** term_months / ( (1 + interest_month) ** term_months - 1 )

def pmt2(principal, principal_left, interest_month, term_months):
    return principal / term_months + principal_left * interest_month


# payment = pmt(principal, interest_monthly, term_months)
# interest_part = principal * interest_monthly
# principal_part = payment - interest_part
# principal_remain = principal - principal_part
# print(payment)
# payment2 = pmt(principal_remain, interest_monthly, term_months - 1)
# print(payment2)