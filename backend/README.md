# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database Locally

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Set up the Database in Docker Container

Alternatively to having Postgres running locally, you can start up the Postgres as Docker container.

Note: For this you will need to download Docker Desktop for running dockers images locally from https://www.docker.com/.

To start Postgres in Docker with the DB automatically populated run the following commands from the root of the project:

```bash
cd _docker-image
docker compose up
```

To remove docker container run:

```bash
docker compose down
```

### Configure .env variables

As per `.envExample` file, create `.env` file and fill in all the necessary variables for the database connection.

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Testing

To deploy the tests, run

- if the Postgres DB is running locally:

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

- if Postgres DB is running as Docker:

```bash
docker compose down # to remove the container and any stored data if needed
docker compose up # to start docker container with seeded data
python test_flaskr.py
```

## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys. 

### Error Handling
Errors are returned as JSON objects in the following format:
```json
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable 

### Endpoints 
#### GET /categories
- Fetches categories in which the keys are the ids and the value is the corresponding string of the category type.
- Request Arguments: None
- Returns: An object with keys:
    - `categories` - list of objects `id: category_string` key: value pairs,
    - `success` - indicates if a response was successful, `boolean` value,
    - `total_categories` - number of total categories, `number` value.
- Sample: `curl http://127.0.0.1:5000/categories`
- Response sample:
```json
{
  "categories": [
    {
      "id": 1, 
      "type": "Science"
    }, 
    {
      "id": 2, 
      "type": "Art"
    }, 
    {
      "id": 3, 
      "type": "Geography"
    }, 
    {
      "id": 4, 
      "type": "History"
    }, 
    {
      "id": 5, 
      "type": "Entertainment"
    }, 
    {
      "id": 6, 
      "type": "Sports"
    }
  ], 
  "success": true, 
  "total_categories": 6
}
```

#### GET /questions
- Fetches paginated questions, categories and current category.
- Request Arguments: `page` - choose page number, starting from 1, default value if the argument is not passed is also 1.
- Returns: An object with keys:
    - `categories` - list of objects `id: category_string` key: value pairs,
    - `current_category` - current selected category object `id: category_string` key: value pair,
    - `questions` - list of objects with keys `id, answer, category, difficulty, question`,
    - `success` - indicates if a response was successful, `boolean` value,
    - `total_questions` - number of total question, `number` value.
- Sample: `curl http://127.0.0.1:5000/questions`
- Response sample:
```json
{
  "categories": [
    {
      "id": 1, 
      "type": "Science"
    }, 
    {
      "id": 2, 
      "type": "Art"
    }, 
  ], 
  "current_category": {
    "id": 1, 
    "type": "Science"
  }, 
  "questions": [
    {
      "answer": "Lake Victoria", 
      "category": 2, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 2, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ], 
  "success": true, 
  "total_questions": 2
}
```

#### DELETE /questions/{question_id}
- General:
    - Deletes the question of the given `id` if it exists.
- Request Arguments: `question_id`
- Returns: An object with keys:
    - `deleted` - deleted questions id value,
    - `success` - indicates if a response was successful, `boolean` value,
- Sample: `curl -X DELETE http://127.0.0.1:5000/questions/1`
- Response sample:
```json
{
  "deleted": 5, 
  "success": true
}
```

#### POST /questions
- General:
    - Creates a new question entry using the submitted question content, category id, difficulty and answer.
- Request Arguments: None
- Returns: An object with keys:
    - `id` - new question's id value,
    - `answer` - answer to the question
    - `category` - question category id value
    - `difficulty` - question difficulty (number)
    - `question` - question content
    - `success` - indicates if a response was successful, `boolean` value,
- Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"Why there are so many tests?","answer":"For Quality!","difficulty":1,"category":1}'`
- Response sample:
```json
{
  "answer": "For Quality!", 
  "category": 1, 
  "difficulty": 1, 
  "question": "Why there are so many tests?", 
  "success": true
  "id": 1
}
```

#### POST /questions/search
- General:
    - Returns questions that match the search term.
- Request Arguments: 
    - body: `{'searchTerm': 'title'}`
- Returns: An object with keys:
    - `current_category` - current selected category,
    - `questions` - list of questions that match the search term,
    - `success` - indicates if a response was successful, `boolean` value,
    - `total_questions` - number of total question, `number` value.
- Sample: `curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"searchTerm":"title"}'`
- Response sample:
```json
{
  "current_category": {
    "id": 1, 
    "type": "Science"
  }, 
  "questions": [
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ], 
  "success": true, 
  "total_questions": 1
}

```

#### GET /categories/{category_id}/questions
- Fetches all questions that match the category id in the request.
- Request Arguments: `category_id` - category id for which to fetch the questions.
- Returns: An object with keys:
    - `categories` - list of objects `id: category_string` key: value pairs,
    - `current_category` - current selected category object `id: category_string` key: value pair,
    - `questions` - list of objects with keys `id, answer, category, difficulty, question`,
    - `success` - indicates if a response was successful, `boolean` value,
    - `total_questions` - number of total question, `number` value.
- Sample: `curl http://127.0.0.1:5000/categories/1/questions`
- Response sample:
```json
{
  "categories": [
    {
      "id": 1, 
      "type": "Science"
    }, 
    {
      "id": 2, 
      "type": "Art"
    }, 
    {
      "id": 3, 
      "type": "Geography"
    }, 
    {
      "id": 4, 
      "type": "History"
    }, 
    {
      "id": 5, 
      "type": "Entertainment"
    }, 
    {
      "id": 6, 
      "type": "Sports"
    }
  ], 
  "current_category": {
    "id": 1, 
    "type": "Science"
  }, 
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }
  ], 
  "success": true, 
  "total_questions": 2
}
```

#### POST /quizzes
- General:
    - Returns random question for a chosen category and that is not in the previous questions list.
- Request Arguments: 
    - body: 
    ```json
    {
      "previous_questions":[10],
      "quiz_category":
      {
        "type":"Art",
        "id": 2
      }
    }
    ```
- Returns: An object with keys:
    - `question` - question object,
    - `success` - indicates if a response was successful, `boolean` value,
- Sample: `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions":[10],"quiz_category":{"type":"Art","id":2}}'`
- Response sample:
```json
{
  "question": {
    "answer": "Mona Lisa", 
    "category": 2, 
    "difficulty": 3, 
    "id": 17, 
    "question": "La Giaconda is better known as what?"
  }, 
  "success": true
}
```