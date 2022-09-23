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
        self.db_user = ''
        self.db_password = ''
        self.db_host = 'localhost:5432'
        self.database_name = "trivia_test"
        self.database_path = 'postgresql://{}:{}@{}/{}'.format(
            self.db_user, self.db_password, self.db_host, self.database_name)
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
    def test_for_get_paginated_question(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['categories']))

    def test_get_questions_above_valid_page(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource does not exists')

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data["categories"])

    def test_nonexistent_category(self):
        res = self.client().get('/categories/7777')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource does not exists')

    def test_delete_question(self):
        new_question = Question(question='new question', answer='new answer', difficulty=1, category=1)
        new_question.insert()
        new_question_id = new_question.id

        res = self.client().delete(f'/questions/{new_question_id}')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == new_question.id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        

    def test_delete_nonexistent_question(self):
        res = self.client().delete('/question/234')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource does not exists')

    def test_add_question(self):
        new_question = {
            'question': 'test question',
            'answer': 'test answer',
            'difficulty': 1,
            'category': 1
        }

        # prev_total_questions = len(Question.query.all())
        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)
        # present_total_questions = len(Question.query.all())

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        # self.assertEqual(prev_total_questions, present_total_questions + 1)

    # def test_add_question_with_incomplete_fields(self):
    #     new_question = {
    #         'question': 'test question',
    #         'answer': 'new answer',
    #         'category': 1
    #     }

    #     res = self.client().post('/questions', json=new_question)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 422)
    #     self.assertEqual(data["success"], False)
    #     self.assertEqual(data["message", 'Error. cannot be processed'])

    def test_search_questions(self):
        searchkeyword = {'searchTerm': 'a'}
        res = self.client().post('/questions/search', json=searchkeyword)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['questions'])
        self.assertIsNotNone(data['total_questions'])

    def test_nonexist_search_term(self):
        searchkeyword = {
            'searchTerm': 'test what @test',
        }
        res = self.client().post('/search', json=searchkeyword)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource does not exists')

    def test_get_questions_basedon_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']), 200)
        # self.assertTrue(data['questions'], total_questions)
        
    def test_nonexist_get_questions_basedon_category(self):
        res = self.client().get('/categories/999/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        # self.assertEqual(data['message'], 'resource does not exists')

    def test_play_quiz(self):
        new_quiz = {
            'previous_questions': [],
            'quiz_category': {
                'type': 'Science',
                'id': 1
            }
        }

        res = self.client().post('/quizzes', json=new_quiz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_play_quiz_invalid_field(self):
        new_quiz = {
            'previous_questions': []
        }
        res = self.client().post('/quizzes', json=new_quiz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], 'the request cannot be processed')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()