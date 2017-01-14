import pytest

from day_rate_to_income import (
    calculate_tax_free_allowance,
    income_tax,
    national_insurance,
)

@pytest.mark.parametrize("pre_tax, expected", [
    (5000, 11000),
    (99000, 11000),
    (110000, 6000),
    (122000, 0),
    (150000, 0),
])
def test_tax_free_allowance(pre_tax, expected):
    assert calculate_tax_free_allowance(pre_tax) == expected


@pytest.mark.parametrize("pre_tax, expected", [
    (5000, 0),
    (10000, 0),
    (20000, 1800),
    (45000, 7200),
    (99000, 28800),
    (100000, 29200),
    (100001, 29200.60),
    (105000, 32200),
    (110000, 35200),
    (160000, 58100),
])
def test_income_tax(pre_tax, expected):
    assert abs(income_tax(pre_tax) - expected) < 100

@pytest.mark.parametrize("pre_tax, expected", [
    (5000, 0),
    (10000, 232.80),
    (20000, 1432.80),
    (45000, 4232.80),
    (99000, 5312.80),
    (110000, 5532.80),
    (160000, 6532.80),
])
def test_ni(pre_tax, expected):
    assert abs(national_insurance(pre_tax) - expected) < 0.01
