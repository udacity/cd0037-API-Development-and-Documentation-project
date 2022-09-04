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
        self.database_path = "postgresql://{}/{}".format('student:student@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {"question": "Say my name!", "answer": "Shino", "difficulty": "1", "category": "3"}

        self.new_question2 = {"question": "Hello World!", "answer": "programming", "difficulty": "1", "category": "1"}

        self.searchTermExistQuestion = {"searchTerm": "Say my"}

        self.searchTermNotExistQuestion = {"searchTerm": "Lona"}

        self.play_quiz1 = {"previous_questions": [5, 9], "quiz_category": {"type": "History", "id": "4"} }

        self.play_quiz2 = {"previous_questions": [5, 9, 12, 23], "quiz_category": {"type": "History", "id": "4"} }


        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass
# =============================================================================================
# READ Section
# =============================================================================================
    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_paginated_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["current_category"], None)
        self.assertTrue(len(data["categories"]))
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["total_questions"])

    def test_404_requesting_beyond_valid_page(self):
        res = self.client().get("/questions?page=1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["message"], "resource not found")
        self.assertFalse(data["success"])

# =============================================================================================
# CREATE Section
# =============================================================================================

    # it will keep adding the same question everytime this test is working !!
    # def test_create_new_questions(self):
    #     res = self.client().post("/questions", json=self.new_question)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data["success"])
    #     self.assertTrue(data["created"])

    def test_400_if_creating_question_fails_because_missing_info(self):
        res = self.client().post("/questions", json=None)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["error"], 400)
        self.assertEqual(data["message"], "bad request")
        self.assertFalse(data["success"])        

# =============================================================================================
# DELETE Section
# =============================================================================================

    # you have to delete an existing question to get this test working !!
    # def test_delete_existing_question(self):
    #     res = self.client().delete("/questions/10")
    #     data = json.loads(res.data)

    #     question = Question.query.filter(Question.id == 10).one_or_none()

    #     self.assertEqual(res.status_code, 422)
    #     self.assertTrue(data["success"])
    #     self.assertEqual(data["deleted"], 10)

    def test_422_delete_non_existing_question(self):
        res = self.client().delete("/questions/1000")
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 10).one_or_none()

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["error"], 422)
        self.assertEqual(data["message"], "unprocessable")
        self.assertFalse(data["success"])

# =============================================================================================
# SEARCH Section
# =============================================================================================

    def test_search_existing_question(self):
        res = self.client().post("/questions", json=self.searchTermExistQuestion)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data["questions"]), 3) # 3 is the number of question with the value "Say my" (partial search)
        self.assertTrue(data["total_questions"])
        self.assertEqual(data["current_category"], None)

    def test_404_search_not_existing_question(self):
        res = self.client().post("/questions", json=self.searchTermNotExistQuestion)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["message"], "resource not found")
        self.assertFalse(data["success"])

# =============================================================================================
# Quizz Section
# =============================================================================================

    def test_play_quiz(self):
        res = self.client().post("/quizzes", json=self.play_quiz1)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data["question"]), 5) # 5 because it will return a json response with 5 pairs in it (answer, question, category, difficulty, id)

    # it should return None in data["question"]
    def test_no_questions_to_play(self):
        res = self.client().post("/quizzes", json=self.play_quiz2)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["question"], None)

# =============================================================================================

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
