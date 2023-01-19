import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def addQuestion(self):
        question = Question(
          question='Who discovered tests?',
          category=1,
          answer='Testers',
          difficulty=4)
        # binds the app to the current context
        with self.app.app_context():
            self.db.session.add(question)
            self.db.session.commit()
            return question.id

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format("student", "student", "localhost:5433", self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_categories(self):
        res = self.client().get("/categories")

        self.assertTrue(res)
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_categories"])
        self.assertTrue(len(data["categories"]))

    def test_get_paginated_questions(self):
        res = self.client().get("/questions")

        self.assertTrue(res)
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["questions"]))
        self.assertTrue(len(data["categories"]))
        self.assertTrue(len(data["current_category"]))

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get("/questions?page=1000")
        self.assertTrue(res)
        self.assertEqual(res.status_code, 404)

        data = json.loads(res.data)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_delete_question(self):
        test_question_id = self.addQuestion()
        res = self.client().delete("/questions/" + str(test_question_id))
        self.assertTrue(res)
        self.assertEqual(res.status_code, 200)

        data = json.loads(res.data)
        question = Question.query.filter(Question.id == test_question_id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], test_question_id)
        self.assertEqual(question, None)

    def test_delete_404_if_question_does_not_exist(self):
        res = self.client().delete("/questions/1000")
        self.assertTrue(res)
        self.assertEqual(res.status_code, 404)

        data = json.loads(res.data)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_delete_422_if_question_param_invalid(self):
        res = self.client().delete("/questions/invalid")
        self.assertTrue(res)
        self.assertEqual(res.status_code, 422)

        data = json.loads(res.data)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_create_new_question(self):
        new_question = {
            "answer": "For Quality!", 
            "category": 1, 
            "difficulty": 1, 
            "question": "Why there are so many tests?"
        }
        res = self.client().post("/questions", json=new_question)
        self.assertTrue(res)
        self.assertEqual(res.status_code, 200)

        data = json.loads(res.data)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["answer"], new_question['answer'])
        self.assertEqual(data["category"], new_question['category'])
        self.assertEqual(data["difficulty"], new_question['difficulty'])
        self.assertEqual(data["question"], new_question['question'])
        self.assertTrue(type(data["id"]) is int)
        # cleanup
        res = self.client().delete("/questions/" + str(data["id"]))


    def test_create_422_new_question(self):
        new_question = {
            "category": 1, 
            "difficulty": 1, 
            "question": "Why there are so many tests?"
        }
        res = self.client().post("/questions", json=new_question)
        self.assertTrue(res)
        self.assertEqual(res.status_code, 422)

        data = json.loads(res.data)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_search_questions_with_matching_search_term_returns_results(self):
        search_term = {'searchTerm': 'title'}
        res = self.client().post("/questions/search", json=search_term)
        self.assertTrue(res)
        self.assertEqual(res.status_code, 200)

        data = json.loads(res.data)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["questions"]))
        self.assertTrue(len(data["current_category"]))

    def test_search_questions_with_empty_search_term_returns_all_questions(self):
        search_term = {'searchTerm': ''}
        res = self.client().post("/questions/search", json=search_term)
        self.assertTrue(res)
        self.assertEqual(res.status_code, 200)

        data = json.loads(res.data)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["questions"]))
        self.assertTrue(len(data["current_category"]))

    def test_search_questions_with_non_matching_search_term_returns_0_results(self):
        search_term = {'searchTerm': 'random_non_existing_string'}
        res = self.client().post("/questions/search", json=search_term)
        self.assertTrue(res)
        self.assertEqual(res.status_code, 200)

        data = json.loads(res.data)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"] == 0)
        self.assertTrue(len(data["questions"]) == 0)
        self.assertTrue(len(data["current_category"]))

    def test_get_questions_by_existing_category(self):
        category_id = 1
        expected_current_category = {'id': 1, 'type': 'Science'}
        res = self.client().get("/categories/" + str(category_id) + "/questions")

        self.assertTrue(res)
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["current_category"])
        self.assertEqual(data["current_category"], expected_current_category)
        self.assertTrue(len(data["categories"]))
        self.assertTrue(data["total_questions"])

    def test_404_get_questions_by_nonexisting_category(self):
        category_id = 100
        res = self.client().get("/categories/" + str(category_id) + "/questions")
        self.assertTrue(res)
        self.assertEqual(res.status_code, 404)

        data = json.loads(res.data)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_422_get_questions_by_invalid_category(self):
        category_id = 'invalid'
        res = self.client().get("/categories/" + str(category_id) + "/questions")
        self.assertTrue(res)
        self.assertEqual(res.status_code, 422)

        data = json.loads(res.data)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_post_quizzes_start_game_with_valid_category(self):
        expected_category_id = 1
        post_body = {"previous_questions":[],"quiz_category":{"type":"Art","id":expected_category_id}}
        res = self.client().post("/quizzes", json=post_body)

        self.assertTrue(res)
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"])
        actual_question = data["question"]
        self.assertEqual(actual_question["category"], expected_category_id)

    def test_post_quizzes_start_game_with_all_category(self):
        expected_category_id = 0
        post_body = {"previous_questions":[],"quiz_category":{"type":"all","id":expected_category_id}}
        res = self.client().post("/quizzes", json=post_body)

        self.assertTrue(res)
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"])

    def test_post_quizzes_with_prev_questions_returns_different_question(self):
        expected_category_id = 6
        previous_questions = [10]
        post_body = {"previous_questions":previous_questions,"quiz_category":{"type":"Sports","id":expected_category_id}}
        res = self.client().post("/quizzes", json=post_body)

        self.assertTrue(res)
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"])
        actual_question = data["question"]
        self.assertEqual(actual_question["category"], expected_category_id)
        self.assertNotEqual(actual_question["id"], previous_questions[0])

    def test_404_post_quizzes_start_game_with_invalid_category(self):
        expected_category_id = 100
        post_body = {"previous_questions":[],"quiz_category":{"type":"invalid","id":expected_category_id}}
        res = self.client().post("/quizzes", json=post_body)

        self.assertTrue(res)
        self.assertEqual(res.status_code, 404)
        data = json.loads(res.data)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()