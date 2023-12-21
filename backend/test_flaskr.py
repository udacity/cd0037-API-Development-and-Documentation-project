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
        response = self.client().delete('/questions/100')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json()['success'], False)
        self.assertEqual(response.get_json()['message'], 'Resource not found')



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()