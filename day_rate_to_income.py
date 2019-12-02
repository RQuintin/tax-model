#!/usr/bin/env python3

import matplotlib

# matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import pandas as pd

# FY 2018/2019
WORKING_DAYS_IN_A_YEAR = 225
FLAT_RATE_VAT = 0.165
VAT_RATE = 0.2
CORPORATION_TAX_RATE = 0.19
NI_PRIMARY_THESHOLD = 702 * 12
NI_UPPER_EARNINGS_LIMIT = 3863 * 12
TAX_FREE_ALLOWANCE = 11850


def charged_vat(income: float) -> float:
    return income * VAT_RATE


def paid_vat(income: float) -> float:
    return income * FLAT_RATE_VAT


def corporation_tax(income: float) -> float:
    return income * CORPORATION_TAX_RATE


def contractor_personal_taxes(pre_tax: float) -> float:
    # Assume we pay out salary to the NI Primary Threshold, which is the
    # effective "tax free rate" for contractors
    untaxed = pre_tax
    personal_taxes: float = 0

    untaxed -= NI_PRIMARY_THESHOLD

    # 2,000 of dividends tax free
    untaxed -= 2000

    basic_rate_eligible = min(untaxed, 50000 - NI_PRIMARY_THESHOLD)
    personal_taxes += basic_rate_eligible * 0.075
    untaxed -= basic_rate_eligible

    higher_rate_eligible = min(untaxed, 100 * 1000)
    personal_taxes += higher_rate_eligible * 0.4
    untaxed -= higher_rate_eligible

    additional_rate_eligible = untaxed
    personal_taxes += additional_rate_eligible * 0.45
    untaxed -= additional_rate_eligible

    return personal_taxes


def calculate_tax_free_allowance(pre_tax):
    if pre_tax < 100000:
        return min(TAX_FREE_ALLOWANCE, pre_tax)
    else:
        return max(0, TAX_FREE_ALLOWANCE - ((pre_tax - 100000) / 2))


def income_tax(pre_tax: float) -> float:
    income_tax_payable: float = 0
    untaxed = pre_tax

    tax_free_allowance = calculate_tax_free_allowance(pre_tax)
    untaxed -= tax_free_allowance

    basic_rate_eligible = min(untaxed, 34_500)
    basic_rate_tax = basic_rate_eligible * 0.2
    income_tax_payable += basic_rate_tax
    untaxed -= basic_rate_eligible

    higher_rate_eligible = min(untaxed, 150_000 - 34_500)
    higher_rate_tax = higher_rate_eligible * 0.4
    income_tax_payable += higher_rate_tax
    untaxed -= higher_rate_eligible

    additional_rate_eligible = untaxed
    additional_rate_tax = untaxed * 0.45
    income_tax_payable += additional_rate_tax

    return income_tax_payable


def national_insurance(pre_ni):
    earnings_above_pt = max(0, pre_ni - NI_PRIMARY_THESHOLD)
    earnings_above_uel = max(0, pre_ni - NI_UPPER_EARNINGS_LIMIT)
    ni = (earnings_above_pt - earnings_above_uel) * 0.12
    ni += earnings_above_uel * 0.02
    return ni

def employers_national_insurance(pre_ni):
    earnings_above_pt = max(0, pre_ni - NI_PRIMARY_THESHOLD)
    return earnings_above_pt * 0.138

def main():
    DAY_RATE_COLNAME = "Day rate (£)"
    PRE_TAX_INCOME_COLNAME = "Pre-tax income"
    CONTRACTOR_TAKE_HOME_COLNAME = "Contractor_take_home"
    E_TAKE_HOME_COLNAME = "Employee take home"

    df = pd.DataFrame(
        data=[
            (day_rate, day_rate * WORKING_DAYS_IN_A_YEAR)
            for day_rate in range(0, 1000, 10)
        ],
        columns=(DAY_RATE_COLNAME, PRE_TAX_INCOME_COLNAME),
    )
    df = df.set_index([DAY_RATE_COLNAME])

    df[CONTRACTOR_TAKE_HOME_COLNAME] = df[PRE_TAX_INCOME_COLNAME] + df[
        PRE_TAX_INCOME_COLNAME
    ].apply(charged_vat)
    df[CONTRACTOR_TAKE_HOME_COLNAME] -= df[PRE_TAX_INCOME_COLNAME].apply(paid_vat)
    df[CONTRACTOR_TAKE_HOME_COLNAME] -= df[PRE_TAX_INCOME_COLNAME].apply(
        corporation_tax
    )
    df[CONTRACTOR_TAKE_HOME_COLNAME] -= df[PRE_TAX_INCOME_COLNAME].apply(
        contractor_personal_taxes
    )

    df[E_TAKE_HOME_COLNAME] = df[PRE_TAX_INCOME_COLNAME] - df[PRE_TAX_INCOME_COLNAME].apply(income_tax)
    df[E_TAKE_HOME_COLNAME] -= df[PRE_TAX_INCOME_COLNAME].apply(national_insurance)

    df["Employee take home (incl employer's NI)"] = df[E_TAKE_HOME_COLNAME]
    df["Employee take home (incl employer's NI)"] -= df[E_TAKE_HOME_COLNAME].apply(employers_national_insurance)

    fig, ax = plt.subplots()

    axes = plt.gca()
    axes.set_ylim([0, 250 * 1000])

    df.plot(title="Contractor income compared to employee income (FY 2018/19)", ax=ax)
    plt.grid()
    plt.savefig("day_rate_to_income.png")


if __name__ == "__main__":
    main()
