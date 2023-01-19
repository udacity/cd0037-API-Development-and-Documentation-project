## Trivia App

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

Completing this trivia app will give you the ability to structure plan, implement, and test an API - skills essential for enabling your future applications to communicate with others.

## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys. 

### Error Handling
Errors are returned as JSON objects in the following format:
```
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
```
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
```
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
```
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
```
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
```
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
```
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
    - body: `{"previous_questions":[10],"quiz_category":{"type":"Art","id":2}}`
- Returns: An object with keys:
    - `question` - question object,
    - `success` - indicates if a response was successful, `boolean` value,
- Sample: `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions":[10],"quiz_category":{"type":"Art","id":2}}'`
- Response sample:
```
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

## About the Stack

### Backend

The [backend](./backend/README.md) directory contains a Flask and SQLAlchemy server. The `__init__.py` contains all the API endpoints logic and the `test_flaskr.py` contains the unit tests:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

> View the [Backend README](./backend/README.md) for more details.

### Frontend

The [frontend](./frontend/README.md) directory contains a complete React frontend to consume the data from the Flask server.

> View the [Frontend README](./frontend/README.md) for more details.
