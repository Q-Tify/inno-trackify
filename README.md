![Lint](https://github.com/Q-Tify/inno-trackify/actions/workflows/lint.yml/badge.svg?branch=actions)
[![Flake8 Status](https://q-tify.github.io/inno-trackify/main/reports/badges/flake8.svg)](https://q-tify.github.io/inno-trackify/main/reports/flake8/index.html)
# inno-trackify

To run service manually:
```
make run
```

To run the backend:
```
poetry run uvicorn app.main:app --reload
```

To run the frontend:
```
poetry run streamlit run frontend/1_🏠_Home.py
```

## Using Swagger UI for API Documentation

Once the backend is running, you can access the Swagger UI to explore the API documentation:

1. Open your web browser and navigate to `http://localhost:8000/docs` (assuming the backend is running on the default port).
2. You will be presented with the Swagger UI interface, where you can see all the available endpoints, their parameters, request/response schemas, and even test them interactively.
3. Click on any endpoint to expand it and view detailed information.
4. You can also try out the endpoints by clicking the "Try it out" button, filling in the required parameters, and clicking "Execute".

You can now use Swagger UI to understand and interact with the API endpoints provided by the inno-trackify backend.

