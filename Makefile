VENV_DIR = .venv
PYTHON = python3
PYTEST = $(VENV_DIR)/bin/pytest
TEST_DIR := tests
SRC_DIR := src

.PHONY: start ruff-linter ruff-linter-fix ruff-formatter

start:
	$(PYTHON) run.py

ruff-linter:
	ruff check .

ruff-linter-fix:
	ruff check --fix .

ruff-formatter:
	ruff format .
