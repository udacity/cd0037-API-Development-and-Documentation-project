## API Reference

### Getting Started
- Base URL: Currently this app is only configured to run locally. Backend app is hosted in `http://127.0.0.1:5000/`, set as a proxy in the frontend config. 
- Authentication: No authentication or API keys.

### Error Handling
Errors are JSON responses formatted in the following:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The following are error codes that can potentially be returned by the API:
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable 

### Endpoints 
#### GET /categories
- General:
    - Returns a list of question categories, success value, and total number of categories
- Sample: `curl http://127.0.0.1:5000/categories`

``` {
  "categories": [
    {
      "type": "Geography",
      "id": 1,
    },
    {
      "type": "History",
      "id": 2,
    }
  ],
  "success": true,
  "total_categories": 2
}
```

#### GET /questions
- General:
    - Returns a list of questions, success value, and total number of questions
    - Results are paginated in groups of 10. Include 'page' argument to choose page number, starting from 1. 
- Sample: `curl http://127.0.0.1:5000/questions`
- Pagination Sample: `curl http://127.0.0.1:5000/questions?page=1`

``` {
  "questions": [
    {
      "answer": "Maya Angelou",
      "id": 5,
      "difficulty": 2,
      "category": 4,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Muhammad Ali",
      "id": 9,
      "difficulty": 1,
      "category": 4,
      "question": "What boxer's original name is Cassius Clay?"
    }
  ],
  "success": true,
  "total_questions": 2
  }
```

#### POST /questions
- General:
    - Creates a new question, which requires the question text, answer text, difficulty score, and category. Returns the id of the question created, and it's success state. If invalid arguments are provided it will return an error response with code 400.
- Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"Who was the first man on the moon?", "answer":"Neil Strongarm", "difficulty":"1", "category":"4"}'`
```
{
  "created": 26,
  "success": true
}
```
#### DELETE /questions/{question_id}
- General:
    - Deletes a question with the given ID. Returns the id of the deleted question, success value, and total questions.
- Sample: `curl -X DELETE http://127.0.0.1:5000/questions/16`
```
{
  "deleted": 16,
  "success": true,
  "total_questions": 15
}
```
#### POST /questions/search
- General:
    - Provides a list of questions based on a search term provided.
- Sample: `curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d "search":"sample"`
```
"questions": [
    {
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }
  ],
  "success": true
```

#### GET /categories/<int:category_id>/questions
- General:
    - Retrieves a list of questions based on a category provided.
- Sample: `curl "http://127.0.0.1:5000/categories/4/questions"`
```
{
  "count": 2,
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
    }
  ]
}
```