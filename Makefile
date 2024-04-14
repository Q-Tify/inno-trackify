install:
	poetry install

create-db: install
	sqlite3 inno-trackify.db < ./migrations/init.sql

run-server: install create-db
	cd ./backend && poetry run uvicorn app.main:app --reload

run-frontend: install create-db
	poetry run streamlit run frontend/1_🏠_Home.py

run: install create-db
	cd ./backend && poetry run uvicorn app.main:app --reload & 
	poetry run streamlit run frontend/app.py
