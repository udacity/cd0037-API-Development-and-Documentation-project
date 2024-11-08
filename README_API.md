Getting Started
	Install the dependencies for the project:
        Run the commands: pip3 install -r requirements.txt from the directory "./backend" and npm install from the directory "./forntend"

    To start the backend server:
        Run the command: flask run --reload from the directory "./backend"
    To start the frontend server:
        Run the command: npm start from the directory "./frontend"

    Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000/, which is set as a proxy in the frontend configuration.
    Authentication: This version of the application does not require authentication or API keys.

Error Handling

Errors are returned as JSON objects in the following format:

{
    "success": False, 
    "error": 400,
    "message": "bad request"
}

The API will return four error types when requests fail:

    400: Bad Request
    404: Resource Not Found
    422: Not Processable
    405: Method Not Allowed

Endpoints
GET /categories
    General:
        Returns a list of all categories, if no categories are found it returns an 404 error       
    Sample: curl -L "http://localhost:5000/categories"
	
	"categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    }
	
	
GET	/questions
	General:
        Returns a list of questions based on the the cuurent category, if no questions are found for that category it returns an 404 error
		Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.	
    Sample: curl -L "http://localhost:5000/questions"
	
	{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "current_category": "Science",
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
        },
        {
            "answer": "Blood",
            "category": 1,
            "difficulty": 4,
            "id": 22,
            "question": "Hematology is a branch of medicine involving the study of what?"
        }
    ],
    "total_questions": 20
	}
	
DELETE /questions/<int:question_id>
	General:
	 Deletes a question based on its id , then returns the deleted question id and a list of questions , if the question to be deleted is not found in the database it returns an 404 error
	 Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.	
	 Sample: curl -L -X DELETE "http://localhost:5000/questions/25"
		
		{
		"deleted": 25,
		"question": [
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
		}
	]
}

POST /questions
	General:
	 Adds a question to the database, returns a list of questions based on the category of the new question , if no questions are found in the database it returns an 404 error
	 Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.	
	 Sample: curl -L "http://localhost:5000/questions" -H "Content-Type: application/json" -d "{
    \"question\":\"In what year did the Titanic sink?\",
    \"answer\":\"1912\",
    \"category\":4,
    \"difficulty\":2
	}"
	 
	 {
    "created": 29,
    "question": [
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
            "answer": "1912",
            "category": 4,
            "difficulty": 2,
            "id": 28,
            "question": "In what year did the Titanic sink?"
        },
        {
            "answer": "1912",
            "category": 4,
            "difficulty": 2,
            "id": 29,
            "question": "In what year did the Titanic sink?"
        }
    ]
}

POST /questions
	General:
	 Searchs the database for a question, returns a list of questions based on the search term 
	 Sample: curl -L "http://localhost:5000/questions" -H "Content-Type: application/json" -d "{
    \"searchTerm\":\"title\"}"
	
	{
    "questions": [
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
			}
		]
	}

GET /categories/<int:category_id>/questions
	General:
	 Gets questions based on the categories id , returns a list of questions based on the category , if no questions are found in the database then returns an 404 error
	 Sample: curl -L "http://localhost:5000/categories/3/questions"
	
	{
    "current_category": "Geography",
    "questions": [
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
    "total_questions": 3
}

POST /quizzes
	General:
	 Gets a question based on previous questions and category , returns a random question of the same category , if no questions are found in the database then returns an 404 error
	 Sample: curl -L "http://localhost:5000/quizzes" -H "Content-Type: application/json" -d "{\"previous_questions\": [1],\"quiz_category\":{\"id\": 1}}"
	
	{
    "question": {
        "answer": "Alexander Fleming",
        "category": 1,
        "difficulty": 3,
        "id": 21,
        "question": "Who discovered penicillin?"
    }
}

