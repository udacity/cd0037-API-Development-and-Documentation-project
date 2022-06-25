import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

from dotenv import load_dotenv

# look for a file named .env and load my database username and password
load_dotenv()

# get hidden username and password from local environment. See env_example for more info
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            DB_USERNAME, DB_PASSWORD, "localhost:5432", self.database_name
        )
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_question = {
            "question": "Who is the best programmer of all time?",
            "answer": "Fodela",
            "category": 4,
            "difficulty": 1,
        }
        self.bad_question = {
            "question": None,
            "answer": None,
            "category": None,
            "difficulty": None,
        }
        self.search_term = {
            "searchTerm":"who"
        }
        self.bad_search_term = {
            "searchTerm":None
        }
        self.quiz_data =  {
            "quiz_category": {"id": 0},
            "previous_questions": [1, 2]
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_paginated_categories(self):
        # get all categories data
        res = self.client().get("/categories")

        # convert data into json format
        data = json.loads(res.data)

        # Check validity of the data
        # Check success
        self.assertEqual(data["success"], True)
        # Check status code
        self.assertEqual(res.status_code, 200)
        # Ensure that there are categories
        self.assertTrue(len(data["categories"]))


    def test_get_all_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        # check validity of the data
        self.assertEqual(data["success"], True)
        # Check status code
        self.assertEqual(res.status_code, 200)
        # Ensure that there are questions
        self.assertTrue(len(data["questions"]))
    
    def test_404_sent_beyond_valid_page(self):
        res = self.client().get("/questions?page=9999")
        data = json.loads(res.data)

        self.assertEqual(data['success'], False)
        # check error code
        self.assertEqual(res.status_code, 404)
        # check message
        self.assertEqual(data["message"], "resource not found : No questions on requested page")

    def test_delete_specific_question(self):
        last_question_id = Question.query.all()[-1].format()["id"]
        res = self.client().delete(f"/questions/{last_question_id}")
        data = json.loads(res.data)

        deleted_question = Question.query.filter(Question.id == 5).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], last_question_id)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["questions"]))
        self.assertEqual(deleted_question, None)

    def test_404_book_to_be_deleted_does_not_exist(self):
        res = self.client().delete("/questions/9999")
        data = json.loads(res.data)

        self.assertEqual(data['success'], False)
        # check error code
        self.assertEqual(res.status_code, 404)
        # check message
        self.assertEqual(data["message"], "resource not found : Question with id: 9999 does not exist")

    def test_post_new_question(self):
        res = self.client().post("/questions", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(data["success"], True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["created"])
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["total_questions"])

    def test_400_if_question_detail_is_missing(self):
        res = self.client().post('/questions', json=self.bad_question)
        data = json.loads(res.data)

        self.assertEqual(data['success'], False)
        # check error code
        self.assertEqual(res.status_code, 400)
        # check message
        self.assertEqual(data["message"], "bad request : A detail of the new question is not defined")

    def test_search_questions(self):
        res = self.client().post("questions/results",json=self.search_term)
        data = json.loads(res.data)

        self.assertEqual(data["success"], True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["categories"]))

    def test_400_undefined_search_term(self):
        res = self.client().post("questions/results", json=self.bad_search_term)
        data = json.loads(res.data)

        self.assertEqual(data['success'], False)
        # check error code
        self.assertEqual(res.status_code, 400)
        # check message
        self.assertEqual(data["message"], "bad request : Search term is undefined")
        

    def test_get_questions_by_category(self):
        res = self.client().get("/categories/1/questions")
        data = json.loads(res.data)

        self.assertEqual(data["success"], True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["total_questions"]) 

    def test_404_if_category_does_not_exist(self):
        res = self.client().post("questions/results", json=self.bad_search_term)
        data = json.loads(res.data)

        self.assertEqual(data['success'], False)
        # check error code
        self.assertEqual(res.status_code, 400)
        # check message
        self.assertEqual(data["message"], "bad request : Search term is undefined")

    def test_get_quiz_questions(self):
          
        res = self.client().post("/quizzes", json=self.quiz_data)
        data = json.loads(res.data)

        self.assertEqual(data["success"], True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data["question"]))
        # Ensure that a question is not repeated
        self.assertTrue(data["question"]["id"] not in data["previous_questions"])

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
