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
        self.database_name = "trivia_test"
        self.database_path = 'postgresql://{}:{}@{}/{}'.format(
            "student", "student", "localhost:5432", self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {"question": "Who is the best football player in the world ?",
                             "answer": "Lionel Messi", "category": 6, "difficulty": 1}
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

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
        self.assertEqual(data["success"], True)

    def test_get_paginate_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data['questions']))
        self.assertIsNone(data["current_category"])
        self.assertTrue(data["categories"])

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get("/questions?page=100", json={"difficulty": 1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_delete_question(self):
        res = self.client().delete("/questions/11")
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 11).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], 11)
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["total_questions"])
        self.assertEqual(question, None)

    def test_422_if_questions_does_not_exist(self):
        res = self.client().delete("/questions/1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_add_new_question(self):
        res = self.client().post("/questions", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["added"])
        self.assertTrue(len(data["questions"]))

    def test_405_if_question_adding_not_allowed(self):
        res = self.client().post("/questions/100", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")

    def test_get_question_search_with_results(self):
        res = self.client().post(
            "/questions/search", json={"searchTerm": "Whose"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertEqual(len(data["questions"]), 1)

    def test_get_question_search_without_results(self):
        res = self.client().post(
            "/questions/search", json={"searchTerm": "Python programming"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["total_questions"], 0)
        self.assertEqual(len(data["questions"]), 0)

    def test_get_question_by_categories(self):
        res = self.client().get("/categories/2/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data['questions']))
        self.assertTrue(data["current_category"])

    def test_get_questions_play_quiz(self):
        res = self.client().post('/quizzes',
                                 json={'previous_questions': [],
                                       'quiz_category':
                                       {'id': '6', 'type': 'Sport'}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['question'])
        self.assertEqual(data['question']['category'], 6)

    def test_404_get_questions_play_quiz(self):
        res = self.client().post('/quizzes',
                                 json={
                                     'previous_questions': []
                                 })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
