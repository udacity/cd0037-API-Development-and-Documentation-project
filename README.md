# Trivia App

Trivia App  provides users the opportunity to test their knowledge by answering a questions based on preselected categories. The app is structured in form of a game which keeps track of score count and delivers a final score at the end of the game.

# App Features Include:

1. Display questions - Questions can be displayed by category. Question difficulty is also displayed. The questions are displayed in a paginated list. Answers are hidden by default.
2. Delete questions - Unwanted questions can be deleted from the list.
3. New Questions casn be added.
4. Search functionality for questions.
5. Play the quiz game! Random mode or selecting a specific category are available as features.

# Getting Started

- The current version of the app can only be run locally. Run the backend app at http://127.0.0.1:5000/
- No authentication is required for the current version of the app. 
- Features like highscores, number of quizzes taken and leaderboard are also not available but planned for a later update.

# Status codes

| Code          | Message            | Meaning/Summary   
| ------------- | ------------------ | --------------------------------------------------------------------------------------------- |
| 200           | OK                 | Everything works fine                                                                         |
| 400           | bad request        | The request was unacceptable, often due to missing required parameter.                        |
| 404           | Resource not found | The Resource does not exist                                                                   |
| 405           | Method not allowed | The wrong method was used or method not supported                                             |
| 408           | Request timeout    | Request took too long to execute                                                              |      
| 422           | Unprocessable      | The request entity was correct but the server was unable to process the contained information |

### Sample response

```
{
  "error": 400,
  "message": "bad request",
  "success": false
}
```

# Endpoints
GET  /questions
- Returns a paginated list of questions, category of question, total number of question and success value.
- Sample: 
``` 
curl http://127.0.0.1:5000/questions  
```
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": true,
  "questions": [
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
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
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
  "success": true,
  "total_questions": 33
}
```

POST  /questions

- Adds a new question to the questions list using the question information provided, category, difficulty and answer. It also provides a question ID based on the total number of questions in the list.
- If a search term is provided, it returns a question/questions based on the query provided.

- Sample:
```
curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question": "Who scored the most goals in the 2002 FIFA World Cup", "answer": "Ronaldo", "difficulty": 4, "category": 6}' 
```

```
{
  "created": 38,
  "questions": [
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
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
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
  "success": true,
  "total_questions": 33
```
DELETE  /questions/{question ID}
- Returns a success message if the selected question ID exists. It also returns a new total number of questions and questions list.
- Sample:

```
curl -X DELETE http://127.0.0.1:5000/questions/24 
```
```
{
  "deleted": 24,
  "questions": [
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
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
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
  "success": true,
  "total_questions": 32
}
```

GET  /categories
- Returns an oblect of categories, a total number of categories and a success message.
- Sample:

```
curl http://127.0.0.1:5000/categories 
```
```
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

GET  /categories/{category ID}/questions
- Returns a list of questions in the given category.
- Sample: 
```
curl http://127.0.0.1:5000/categories/6/questions 
```
```
{
  "current_category": "Sports",
  "questions": [
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "Roberto Baggio",
      "category": 6,
      "difficulty": 2,
      "id": 24,
      "question": "Who missed the last penalty in the 1994 FIFA World Cup Final"
    },
    {
      "answer": "Ronaldo",
      "category": 6,
      "difficulty": 4,
      "id": 38,
      "question": "Who scored the most goals in the 2002 FIFA World Cup"
    }
  ],
  "success": true,
  "total_questions": 4
}

```
# Testing and Frontend
View the backend and frontend readme files for more details.

# Authors
The fantastic people at Udacity and Myself, Omotola Macaulay.

# Acknowledgements
The awesome team at Udacity, Coach Caryn and all of the students.
