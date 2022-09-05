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

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createbd trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

## Documenting your Endpoints

You will need to provide detailed documentation of your API endpoints including the URL, request parameters, and the response body. Use the example below as a reference. [done]

## Documentation

#### Error Handlers

In our application, we uses conventional JSON object to indicate the success or failure of an API request. It will return JSON response with the following body:

- `error`: indicate the HTTP status code.
- `message`: indicate a short description for the error type.
- `success`: indicate the success or the failure of the request.

Example:
```bash
{
  "error": 404,
  "message": "resource not found",
  "success": false
}
```

Error Types:

- `400`: bad request
- `404`: resource not found
- `405`: method not allowed
- `422`: unprocessable
- `500`: internal server error


#### API endpoints


`GET '/api/v1.0/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```

`GET '/questions'`

- Request Arguments: [Optional] - 'page': determine the page number for questions.
- Returns JSON object with the following body:
   - `categories`: returns a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category.
   - `current_category`: returns 'None' bcause questions are from different categories not just one.
   - `total_questions`: returns the number of questions in all categories.
   - `questions`: returns paginated questions in groups of 10, each with full object description.

`curl http://127.0.0.1:5000/questions` or `curl http://127.0.0.1:5000/questions?page=1`
```json
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": null, 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }, 
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ], 
  "total_questions": 23
}

```

`DELETE '/questions/{question_id}'`

- Request Arguments: 'id' as the question id to be deleted.
- Returns JSON object with the following body:

   - `success`: returns a success value of this request, either true or false.
   - `deleted`: returns id of the deleted question.

`curl http://127.0.0.1:5000/questions/28 -X DELETE`
```json
{
  "deleted": 28, 
  "success": true
}
```


`POST '/questions'`

- Request Arguments: JSON object with the following body:

   - `question`: returns question value as a string.
   - `answer`: returns answer value as a string.
   - `category`: returns category id as a string from 1 to the last category id.
   - `difficulty`: returns difficulty value as a string from 1 to 5.
   - `searchTerm`: returns search value which is case-insensitive and partial search.
 
 There's two features can be run here in this request based on the request argument values.
 if `searchTerm` element doesn't exist in the JSON object from the request argument, it will activiate `create new question` feature using the rest of the request body elements. it will return the following JSON Object body:
 
 - `success`: returns the success value of this request, either true of false.
 - `created`: returns a formatted JSON object to descripe the created question.
  

Otherwise, if `searchTerm` exist in the JSON body from the request argument, it will ignore the rest of the request body and take the value of `searchTerm`, it will search for questions (case-insensitive and partial search) based on the `searchTerm` value.

 - `questions`: returns the resulting questions of this search request as a paginated questions in groups of 10.
 - `total_questions`: returns the number of questions in all categories.
 - `current_category`: returns 'None' value for now, because there's a chance the resulting questions can be from different categories.

### Sample - creating new question
`curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question": "How are you?", "answer": "better than you", "category": "4", "difficulty": "5" }'`
```json
{
  "created": {
    "answer": "better than you", 
    "category": 4, 
    "difficulty": 5, 
    "id": 29, 
    "question": "How are you?"
  }, 
  "success": true
}
```

### Sample - search for questions
`curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm": "how" }'`
```json
{
  "current_category": null, 
  "questions": [
    {
      "answer": "One", 
      "category": 2, 
      "difficulty": 4, 
      "id": 18, 
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }
  ], 
  "total_questions": 22
}
```
`GET '/categories/{category_id}/questions'`

- Fetches questions based on a single category.
- Request Arguments: `category_id` as an integer that represent the category id.
- Returns: JSON object with the following body:

  - `questions`: returns the resulting questions by category as a paginated questions in groups of 10.
  - `total_questions`: returns the number of questions in all categories.
  - `current_category`: returns category type as a string.

`curl http://127.0.0.1:5000/categories/4/questions`

```json
{
  "current_category": "History", 
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Scarab", 
      "category": 4, 
      "difficulty": 4, 
      "id": 23, 
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    }, 
    {
      "answer": "better than you", 
      "category": 4, 
      "difficulty": 5, 
      "id": 29, 
      "question": "How are you?"
    }
  ], 
  "total_questions": 23
}
```
  

`POST '/quizzes'`

- Fetches JSON object with 'question' element which have a value of the next random question, and if there's no coming question, it should return 'None' or 'Null' as the value of 'question' element.
- Request Arguments: JSON object with the following body:

  - `previous_questions`: A list of previous questions IDs.
  - `quiz_category`: A dictionary which have `type` with the value of `category_string` and `id` with the value of `category_id` as a string.

- Returns: JSON object with a single element `question` which have either the value of `None` as there's no coming question or `question object` of the coming random question.

`curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [5, 9], "quiz_category": {"type": "History", "id": "4"} }'`

```json
{
  "question": {
    "answer": "George Washington Carver", 
    "category": 4, 
    "difficulty": 2, 
    "id": 12, 
    "question": "Who invented Peanut Butter?"
  }
}

```


## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
