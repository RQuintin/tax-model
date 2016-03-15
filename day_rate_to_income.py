#!/usr/bin/env python3

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import pandas as pd

WORKING_DAYS_IN_A_YEAR = 225
VAT_RATE = 0.145

def add_charged_vat(income):
    return income * 1.2

def subtract_charged_vat(income):
    return income * (1 - VAT_RATE)

def corporation_tax(income):
    return income - ((income - 10600) * 0.2)

def remove_cash(income):
    tax_free_allowance = 10600
    total = min(income, tax_free_allowance)
    income -= total

    dividend_allowance = min(income, 5000)
    income -= dividend_allowance
    total += dividend_allowance

    basic_rate_eligible = min(income, 38000)
    income -= basic_rate_eligible
    total += basic_rate_eligible * (1 - 0.075)

    higher_rate_eligible = min(income, 43000)
    income -= higher_rate_eligible
    total += higher_rate_eligible * (1 - 0.325)

    additional_rate_eligible = income
    total += additional_rate_eligible * (1 - 0.381)

    return total

def salary_estimate(income):
    return income / (1 - 0.33)

def main():
    df = pd.DataFrame(
        data=[(day_rate, day_rate * WORKING_DAYS_IN_A_YEAR)
           for day_rate in range(300, 640, 20)],
        columns=("day_rate", "gross_income")
    )
    df = df.set_index(["day_rate"])
    df["net_income"] = df["gross_income"].apply(add_charged_vat)
    df["net_income"] = df["net_income"].apply(subtract_charged_vat)
    df["net_income"] = df["net_income"].apply(corporation_tax)
    df["net_income"] = df["net_income"].apply(remove_cash)
    df["employee_gross"] = df["net_income"].apply(salary_estimate)
    fig, ax = plt.subplots()
    df.plot(ax=ax)
    plt.show()

if __name__ == "__main__":
    main()
