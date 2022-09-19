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
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
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

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

    
import os
import unittest
import json
from urllib import response
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from dotenv import load_dotenv
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            "postgres", "beopson", "localhost:5432", self.database_name
        )
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

    """
    DONE
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_all_categories(self):
        response = self.client().get('/categories')
        body = json.loads(response.data)
        self.assertEqual(body['success'], True)
        self.assertTrue(body['categories'])

    def test_get_all_categories_error(self):
        response = self.client().get('/categories/1')
        body = json.loads(response.data)
        self.assertEqual(body['success'], False)
        self.assertEqual(body['error'], 404)
        self.assertEqual(body['message'], "not found")

    def test_get_all_questions(self):
        response = self.client().get('/questions')
        body = json.loads(response.data)
        self.assertEqual(body['success'], True)
        self.assertTrue(body['questions'])

    def test_get_all_questions_error(self):
        response = self.client().get('/questions/1')
        body = json.loads(response.data)
        self.assertEqual(body['success'], False)
        self.assertEqual(body['error'], 405)
        self.assertEqual(body['message'], "Method Not Allowed")

    def test_delete_individual_question(self):
        response = self.client().delete('/questions/22')
        body = json.loads(response.data)
        self.assertEqual(body['success'], True)
        self.assertEqual(body['deleted'], 22)

    def test_delete_individual_question_error(self):
        response = self.client().delete('/questions/1000')
        body = json.loads(response.data)
        self.assertEqual(body['success'], False)
        self.assertEqual(body['error'], 422)
        self.assertEqual(body['message'], 'unprocessable')

    def test_create_individual_question(self):
        test_question = {
            "question": "What is Udacity",
            "answer": "an American for-profit educational organization founded by Sebastian Thrun, David Stavens, and Mike Sokolsky offering massive open online courses. According to Thrun, the origin of the name Udacity comes from the company's desire to be 'audacious for you, the student'.",
            "category": "1",
            "difficulty": "1"

        }
        response = self.client().post('/questions', json=test_question)
        body = json.loads(response.data)
        self.assertEqual(body['success'], True)
        self.assertTrue(body['created'])

    def test_create_individual_question_error(self):
        test_question = {
            "question": "What is Udacity",
            "answer": "",
            "category": "1",
            "difficulty": "1"

        }
        response = self.client().post('/questions', json=test_question)
        body = json.loads(response.data)
        self.assertEqual(body['success'], False)
        self.assertEqual(body['error'], 422)
        self.assertEqual(body['message'], 'unprocessable')

    def test_get_individual_question(self):
        response = self.client().post(
            'questions/search', json={"search_term": "title"})
        body = json.loads(response.data)

        self.assertEqual(body['success'], True)
        self.assertTrue(body['questions'])
        self.assertTrue(body['total_questions'])

    def test_get_individual_question_error(self):
        response = self.client().post(
            'questions/search', json={"search_term": ""})
        body = json.loads(response.data)
        self.assertEqual(body['error'], 422)
        self.assertEqual(body['success'], False)
        self.assertEqual(body['message'], 'unprocessable')

    def test_get_individual_question_by_category(self):
        response = self.client().get('/categories/1/questions')
        body = json.loads(response.data)
        self.assertEqual(body['success'], True)
        self.assertTrue(body['questions'])

    def test_get_individual_question_by_category_error(self):
        response = self.client().get('/categories/1/question')
        body = json.loads(response.data)
        self.assertEqual(body['success'], False)
        self.assertEqual(body['error'], 404)
        self.assertEqual(body['message'], "not found")

    def test_get_individual_question_by_quizes(self):
        test_quiz = {
            'previous_questions': [4, 8],
            'quiz_category': {
                'id': 1,
                'type': 'sport'
            }
        }
        response = self.client().post('/quizes', json=test_quiz)
        body = json.loads(response.data)
        self.assertEqual(body['success'], True)
        self.assertTrue(body['question'])
        self.assertNotEqual(body['question']['id'], 4)
        self.assertNotEqual(body['question']['id'], 8)
        self.assertEqual(body['question']['category'], 1)

    def test_get_individual_question_by_quizes_error(self):
        test_quiz = {
            "previous_questions": [45, 8],
            "quiz_category": {
                "id": 10,
                "type": "sport"
            }
        }
        response = self.client().post('/quizes', json=test_quiz)
        body = json.loads(response.data)
        self.assertEqual(body['error'], 422)
        self.assertEqual(body['success'], False)
        self.assertEqual(body['message'], 'unprocessable')

    def test_not_found(self):
        response = self.client().get('/question')
        body = json.loads(response.data)

        self.assertEqual(body['error'], 404)
        self.assertEqual(body['success'], False)
        self.assertEqual(body['message'], 'not found')

    def test_unprocessable(self):
        test_question = {
            "question": "What is Gombe",
            "answer": "",
            "category": "1",
            "difficulty": ""

        }
        response = self.client().post('/questions', json=test_question)
        body = json.loads(response.data)
        self.assertEqual(body['error'], 422)
        self.assertEqual(body['success'], False)
        self.assertEqual(body['message'], 'unprocessable')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
