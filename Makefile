POETRY_RUN = poetry run

.PHONY: install lint format test run

install:
	poetry install

lint:
	$(POETRY_RUN) ruff check src tests

format:
	$(POETRY_RUN) black src tests
	$(POETRY_RUN) ruff format src tests

test:
	$(POETRY_RUN) pytest

run:
	$(POETRY_RUN) python -m src.main --files data/math.csv data/physics.csv data/programming.csv --report median-coffee

