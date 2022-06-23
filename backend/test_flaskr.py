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

    # def test_delete_specific_question(self):
    #     res = self.client().delete("/questions/5")
    #     data = json.loads(res.data)

    #     deleted_question = Question.query.filter(Question.id == 5).one_or_none()

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertEqual(data["deleted"], 5)
    #     self.assertTrue(data["total_questions"])
    #     self.assertTrue(len(data["questions"]))
    #     self.assertEqual(deleted_question, None)

    def test_post_new_question(self):
        res = self.client().post("/questions", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["total_questions"])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
