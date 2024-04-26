.ONESHELL:
ENV_PREFIX=$(shell python -c "if __import__('pathlib').Path('.venv/bin/pip').exists(): print('.venv/bin/')")

help:             ## Show the help.
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@fgrep "##" Makefile | fgrep -v fgrep

install:          ## Install the project in dev mode.
	poetry install --no-root

run-server: install
	cd ./backend && poetry run uvicorn app.main:app --reload

run-frontend: install
	poetry run streamlit run frontend/app.py

run: install
	cd ./backend && poetry run uvicorn app.main:app --reload & 
	poetry run streamlit run frontend/app.py

lint-black: install ## Run black linter.
	@$(ENV_PREFIX)black -l 79 backend/ frontend/

lint-flake8: install ## Run flake8 linter.
	@$(ENV_PREFIX)flake8 backend/ frontend/ $(ARGS)

test-backend: install ## Run tests.
	@$(ENV_PREFIX)pytest --cov=backend/app --cov-branch --cov-fail-under=85 $(ARGS) backend/tests

lint: lint-black lint-flake8 ## Run all linters.
