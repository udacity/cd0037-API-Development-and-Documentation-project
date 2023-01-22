## Trivia App

Udacity is invested in creating bonding experiences for its employees and students. 

The application has the following features:

1. Displays questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Deletes questions.
3. Adds questions and require that they include question and answer text.
4. Searches for questions based on a text query string.
5. Plays the quiz game, randomizing either all questions or within a specific category.

The full API reference is available in the [backend](./backend/README.md) directory.

## About the Stack

### Backend

The [backend](./backend/README.md) directory contains a Flask and SQLAlchemy server. The `__init__.py` contains all the API endpoints logic and the `test_flaskr.py` contains the unit tests:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

The database is Postgres that can be started either locally or as a docker.

> View the [Backend README](./backend/README.md) for more details.

### Frontend

The [frontend](./frontend/README.md) directory contains a complete React frontend to consume the data from the Flask server.

> View the [Frontend README](./frontend/README.md) for more details.
