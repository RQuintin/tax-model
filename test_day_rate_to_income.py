import pytest

from day_rate_to_income import (
    calculate_tax_free_allowance,
    income_tax,
    national_insurance,
)


@pytest.mark.parametrize(
    "pre_tax, expected",
    [(5000, 5000), (99000, 11850), (110000, 6850), (122000, 850), (150000, 0),],
)
def test_tax_free_allowance(pre_tax, expected):
    assert calculate_tax_free_allowance(pre_tax) == expected


@pytest.mark.parametrize(
    "pre_tax, expected",
    [
        (5000, 0),
        (10000, 0),
        (20000, 1630.00),
        (45000, 6630.00),
        (99000, 27960.00),
        (100000, 28360.00),
        (100001, 28360.60),
        (105000, 31360.00),
        (110000, 34360.00),
        (160000, 57600.00),
    ],
)
def test_income_tax(pre_tax, expected):
    actual = income_tax(pre_tax)
    assert expected == pytest.approx(actual)


@pytest.mark.parametrize(
    "pre_tax, expected",
    [
        (5000, 0),
        (10000, 189.12),
        (20000, 1389.12),
        (45000, 4389.12),
        (99000, 5604.12),
        (110000, 5824.12),
        (160000, 6824.12),
    ],
)
def test_ni(pre_tax, expected):
    actual = national_insurance(pre_tax)
    assert expected == pytest.approx(actual, abs=5)
