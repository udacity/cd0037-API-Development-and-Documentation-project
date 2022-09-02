# Trivia APP 

## API Reference

### Getting Started
Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000/, which is set as a proxy in the frontend configuration.

### Authentication
This version of the application does not require authentication or API keys.

### Error Handling
Errors are returned as JSON objects in the following format:

```json
  {
      "success": False, 
      "error": 400,
      "message": "bad request"
  }
```

### Usage
API endpoints can be invoked using cURL
Example of using cURL for GET request:
curl http://127.0.0.1:5000/categories

### Endpoints
`GET '/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains an object of id: category_string key:value pairs.
***Sample Output***
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
    "success": true
}
```

---

`GET '/questions?page=${integer}'`
***Example***:
curl http://127.0.0.1:5000/questions?page=1


- Fetches a paginated set of questions, a total number of questions, all categories and current category string.
- Request Arguments: `page` - integer
- Returns: An object with 10 paginated questions, total questions, object including all categories, and current category string

***Sample Output***
```json
  {"categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": "Art",
  "questions": [
    {
      "answer": "This is an answer",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "This is a question"
    },
        {
      "answer": "This is an answer",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "This is a question"
    },

  
  ],
  "success": true,
  "total_questions": 30
}


```

---

`GET '/categories/${id}/questions'`
***Example***:
 curl http://127.0.0.1:5000/categories/4/questions


- Fetches questions for a cateogry specified by id request argument
- Request Arguments: `id` - integer
- Returns: An object with questions for the specified category, total questions, and current category string

***Sample Output***
```json
{
  "current_category": "History",
  "questions": [
    {
      "answer": "This is an answer",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "This is a question"
    },
    {
      "answer": "This is an answer",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "This is a question"
    }
  ],
  "total_questions": 2
}

```

---

`DELETE '/questions/${id}'`
***Example***:
curl http://127.0.0.1:5000/questions/17 -X DELETE


- Deletes a specified question using the id of the question
- Request Arguments: `id` - integer
- Returns:  id of the question that has been deleted anf total number of questions that are remaining in the question bank.
```json
{
  "deleted": 14,
  "success": true,
  "total_questions": 28
}

```

---

`POST '/quizzes'`

- Sends a post request in order to get the next question
- Request Body:

```json
{
    'previous_questions': [1, 4, 20, 15]
    quiz_category': 'current category'
 }
```

- Returns: a single new question object

```json
{
  "question": {
    "id": 1,
    "question": "This is a question",
    "answer": "This is an answer",
    "difficulty": 5,
    "category": 4
  },
  "success": true
}
```

---

`POST '/questions'`
***Example***:
 curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"This is a question","answer":"This is an answer","category":"1","difficulty":"4"}'


- Sends a post request in order to add a new question
- In the request body you specify the question, the answer, the difficulty a number between 1-4(inclusive) where one is least difficult and 4 being very difficult
- Request Body:

```json
{
  "question": "Heres a new question string",
  "answer": "Heres a new answer string",
  "difficulty": 1,
  "category": 3
}
```

- Returns: an object with the id of the question that has just been created and the total number of questions in the question bank
***Sample Output***
```json
{
  "created": 60,
  "success": true,
  "total_questions": 30
}


```

---

`POST '/questions/search'`

- Sends a post request in order to search for a specific question by search term
- Request Body:

```json
{
  "searchTerm": "this is the term the user is looking for"
}
```

- Returns: any array of questions, a number of totalQuestions that met the search term and the current category string

```json
  {"current_category": "Art",
  "questions": [
    {
      "answer": "This is an answer",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "This is a question"
    }
  ],
  "success": true,
  "total_questions": 1
}

```
