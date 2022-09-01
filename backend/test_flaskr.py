import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = "postgresql://{}:{}@{}/{}".format(DB_USER, DB_PASSWORD,'localhost:5432', DB_NAME)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
        self.new_question = {
            "question": "Test question",
            "answer": "test answer",
            "difficulty": "1",
            "category": "1"
    }

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue('categories', True)
    
    def test_get_paginated_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["categories"])
        self.assertTrue(data["current_category"])
    
    def test_404_request_beyond_page_limit(self):
        res = self.client().get("/questions?page=100000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_delete_question(self):
        res = self.client().delete("/questions/21")
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 21).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], 21)
        self.assertEqual(question, None)

    def test_422_if_question_does_not_exist(self):
        res= self.client().delete("questions/21")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["message"], "unprocessable entity")
        self.assertEqual(data["success"], False)

    def test_422_if_question_is_out_of_range(self):
        res= self.client().delete("questions/10000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["message"], "unprocessable entity")
        self.assertEqual(data["success"], False)

    def test_add_new_question(self):
        res = self.client().post("/questions", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["categories"])
        self.assertTrue(data["current_category"])

    def test_405_if_add_new_question_not_allowed(self):
        res = self.client().post("/questions/12", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")
    
    def test_get_question_search_with_success(self):
        res = self.client().post("/questions/search", json={"searchTerm":"Who"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["current_category"])

    def test_get_question_search_without_success(self):
        res = self.client().post("/questions/search", json={"searchTerm":"madman"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")
    
    def test_get_question_by_category_with_success(self):
        res = self.client().get("/categories/1/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertEqual(data["current_category"], "Science")
    
    def test_404_get_question_by_category_without_success(self):
        res = self.client().get("/categories/9/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()