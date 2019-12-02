day_rate_to_income.png:
	tox

day_rate_to_income.tar.gz: day_rate_to_income.py test_day_rate_to_income.py requirements.txt mypy.ini
	tar czf $@ $^

all: day_rate_to_income.png day_rate_to_income.tar.gz
