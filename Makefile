.ONESHELL:
ENV_PREFIX=$(shell python -c "if __import__('pathlib').Path('.venv/bin/pip').exists(): print('.venv/bin/')")

ifdef ./source.env
include ./source.env
export $(shell sed 's/=.*//' ./source.env)
endif

help:             ## Show the help.
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@fgrep "##" Makefile | fgrep -v fgrep

install:          ## Install the project in dev mode.
	poetry install --no-root

create-db: install
	sqlite3 inno-trackify.db < ./migrations/init.sql

run-server: install create-db
	cd ./backend && poetry run uvicorn app.main:app --reload --host 0.0.0.0

run-frontend: install
	poetry run streamlit run frontend/1_🏠_Home.py --browser.serverAddress="0.0.0.0"

run: install
	cd ./backend && poetry run uvicorn app.main:app --reload --host 0.0.0.0 & 
	poetry run streamlit run frontend/app.py

lint-black: install ## Run black linter.
	@$(ENV_PREFIX)black -l 79 backend/ frontend/

lint-flake8: install ## Run flake8 linter.
	@$(ENV_PREFIX)flake8 backend/ frontend/ $(ARGS)

test-backend: install ## Run tests.
	@$(ENV_PREFIX)pytest --cov=backend/app --cov-branch $(ARGS) backend/tests

bandit: install ## Run bandit.
	@$(ENV_PREFIX)bandit -r backend/app

lint: lint-black lint-flake8 ## Run all linters.

build-frontend: ## Build the docker image.
	docker build . -t inno-trackify-frontend -f Dockerfile.frontend

build-backend: ## Build the docker image.
	docker build . -t inno-trackify-backend -f Dockerfile.backend
