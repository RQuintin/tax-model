#!/usr/bin/env python3

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import pandas as pd

WORKING_DAYS_IN_A_YEAR = 225
FLAT_RATE_VAT = 0.145
VAT_RATE = 0.2
CORPORATION_TAX_RATE = 0.2


def charged_vat(income):
    return income * VAT_RATE


def paid_vat(income):
    return income * FLAT_RATE_VAT


def corporation_tax(income):
    return income * CORPORATION_TAX_RATE


def dividend_tax(pre_tax):
    # Assume we're paying a salary equal to tax free allowance
    tax_free_allowance = calculate_tax_free_allowance(pre_tax)
    pre_tax -= tax_free_allowance

    # dividend personal allowance
    pre_tax -= min(pre_tax, 5000)

    basic_rate_eligible = min(pre_tax, 43000 - 5000)
    basic_rate_tax = basic_rate_eligible * 0.075
    pre_tax -= basic_rate_eligible

    higher_rate_eligible = min(pre_tax, 150000 - 43000 - 5000)
    higher_rate_tax = higher_rate_eligible * 0.325
    pre_tax -= higher_rate_eligible

    additional_rate_eligible = pre_tax
    additional_rate_tax = additional_rate_eligible * 0.381

    return basic_rate_tax + higher_rate_tax + additional_rate_tax


def calculate_tax_free_allowance(pre_tax):
    if pre_tax < 100000:
        return 11000
    else:
        return max(0, 11000 - ((pre_tax - 100000) / 2))


def income_tax(pre_tax):
    tax_free_allowance = calculate_tax_free_allowance(pre_tax)
    pre_tax -= tax_free_allowance

    basic_rate_eligible = min(pre_tax, 43000 - 11000)
    basic_rate_tax = basic_rate_eligible * 0.2
    pre_tax -= basic_rate_eligible

    higher_rate_eligible = min(pre_tax, 150000 - 43000)
    higher_rate_tax = higher_rate_eligible * 0.4
    pre_tax -= higher_rate_eligible

    additional_rate_eligible = pre_tax

    return basic_rate_tax + higher_rate_tax

def national_insurance(pre_ni):
    ni_free_allowance = 8060
    eligible = min(pre_ni, ni_free_allowance)
    pre_ni -= eligible
    after_ni = eligible

    middle_rate_eligible = min(pre_ni, 43000 - 8060)
    middle_rate_ni = middle_rate_eligible * 0.12
    pre_ni -= middle_rate_eligible

    upper_rate_eligible = pre_ni
    upper_rate_ni = upper_rate_eligible * 0.02

    return middle_rate_ni + upper_rate_ni

def employers_ni(pre_ni):
    ni_free_allowance = 8060
    eligible = min(pre_ni, ni_free_allowance)
    pre_ni -= eligible
    after_ni = eligible

    middle_rate_eligible = min(pre_ni, 43000 - 8060)
    middle_rate_ni = middle_rate_eligible * 0.138
    pre_ni -= middle_rate_eligible

    upper_rate_eligible = pre_ni
    upper_rate_ni = upper_rate_eligible * 0.138

    return middle_rate_ni + upper_rate_ni


def main():
    df = pd.DataFrame(
        data=[
            (day_rate, day_rate * WORKING_DAYS_IN_A_YEAR)
            for day_rate in range(200, 1000, 10)
        ],
        columns=("Day rate (£)", "Pre-tax income")
    )
    df = df.set_index(["Day rate (£)"])
    df["Contractor take home"] = df["Pre-tax income"] + df["Pre-tax income"].apply(charged_vat)
    df["Contractor take home"] -= df["Pre-tax income"].apply(paid_vat)
    df["Contractor take home"] -= df["Pre-tax income"].apply(corporation_tax)
    df["Contractor take home"] -= df["Pre-tax income"].apply(dividend_tax)

    df["Employee take home"] = df["Pre-tax income"] - df["Pre-tax income"].apply(income_tax)
    df["Employee take home"] -= df["Pre-tax income"].apply(national_insurance)
    df["Employee take home"] -= df["Pre-tax income"].apply(national_insurance)

    fig, ax = plt.subplots()

    df.plot(
        title="Contractor income compared to employee income (FY 2016/17)",
        ax=ax
    )
    plt.show()

if __name__ == "__main__":
    main()
