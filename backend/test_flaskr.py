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
        self.new_question = {
            'category': 1,
            'question': 'Test Question Post',
            'answer': 'Test Answer Post',
            'difficulty': 1
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

            # Add test data here
            test_question = Question(question="Test Question", answer="Test Answer", category=1, difficulty=1)
            self.db.session.add(test_question)
            self.db.session.commit()

            # Store the test question ID for use in tests
            self.test_question_id = test_question.id

    def tearDown(self):
        """Executed after reach test"""
        with self.app.app_context():
            self.db.session.remove()
            self.db.drop_all()

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories(self):
        """Test GET request for all available categories"""

        # Make a GET request to the /categories endpoint
        response = self.client().get('/categories')
        data = response.get_json()

        # Check if the categories match the expected categories
        expected_categories = {
            '1': "Science",
            '2': "Art",
            '3': "Geography",
            '4': "History",
            '5': "Entertainment",
            '6': "Sports"
        }
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertDictEqual(data['categories'], expected_categories)
        self.assertEqual(data['number_of_categories'], 6)

    def test_delete_question(self):
        """Test DELETE request for a question by id"""

        # Check that the question exists
        response = self.client().get(f'/questions/{self.test_question_id}')
        self.assertEqual(response.status_code, 200)

        # Make a DELETE request to the /questions endpoint with an existing question id
        response = self.client().delete(f'/questions/{self.test_question_id}')
        self.assertEqual(response.status_code, 200)
        response = self.client().get(f'/questions/{self.test_question_id}')
        self.assertEqual(response.status_code, 404)

    def test_delete_question_not_found(self):
        """Test DELETE request for a question by id that does not exist"""
        # Make a DELETE request to the /questions endpoint with a non-existing question id
        response = self.client().delete('/questions/100000')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json()['success'], False)
        self.assertEqual(response.get_json()['message'], 'Resource not found')

    def test_post_question(self):
        """Test POST request for a new question"""
        # Make a POST request to the /questions endpoint with a new question
        response = self.client().post('/questions', data=json.dumps(self.new_question.copy()),
                                      content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()['success'], True)
        # Check that the question exists
        response = self.client().get(f'/questions/{response.get_json()["question_id"]}')
        self.assertEqual(response.status_code, 200)

    def test_post_question_with_missing_data(self):
        # Simulate missing data in the request
        incomplete_data = self.new_question.copy()
        del incomplete_data['answer']  # Removing a required field

        response = self.client().post('/questions', data=json.dumps(incomplete_data), content_type='application/json')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)  # Expect a 500 status code
        self.assertFalse(data['success'])
        self.assertIn('error', data)

    def test_search_questions(self):
        response = self.client().post('/questions/search', json={'searchTerm': 'title'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('questions', data)
        self.assertIsInstance(data['questions'], list)
        # More assertions can be added based on the expected content of the response

    def test_search_questions_no_term(self):
        response = self.client().post('/questions/search', json={})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertFalse(data['success'])
        self.assertIn('error', data)

    def test_get_questions_by_category(self):
        category_id = 1  # Assuming this is a valid category ID
        response = self.client().get(f'/categories/{category_id}/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('questions', data)
        self.assertIsInstance(data['questions'], list)
        # Additional assertions can be added based on the expected content

    def test_get_questions_invalid_category(self):
        invalid_category_id = 9999  # Assuming this is an invalid category ID
        response = self.client().get(f'/categories/{invalid_category_id}/questions')
        self.assertEqual(response.status_code, 404)

    def test_get_paginated_questions(self):
        response = self.client().get('/questions?page=1')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('questions', data)
        self.assertTrue(len(data['questions']) <= 10)
        self.assertIn('total_questions', data)
        self.assertIn('categories', data)

    def test_get_questions_beyond_valid_page(self):
        response = self.client().get('/questions?page=1000')  # Assuming this is beyond available pages
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['questions']), 0)  # No questions should be returned

    def test_get_quiz_question(self):
        request_data = {
            'previous_questions': [],
            'quiz_category': {'id': 1, 'type': 'Science'}
        }
        response = self.client().post('/quizzes', json=request_data)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('question', data)
        self.assertIsNotNone(data['question'])

    def test_quiz_question_exclusion_of_previous_questions(self):
        request_data = {
            'previous_questions': [1, 2, 3],  # Assuming these are IDs of previous questions
            'quiz_category': {'id': 1, 'type': 'Science'}
        }
        response = self.client().post('/quizzes', json=request_data)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('question', data)
        self.assertNotIn(data['question']['id'], request_data['previous_questions'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
