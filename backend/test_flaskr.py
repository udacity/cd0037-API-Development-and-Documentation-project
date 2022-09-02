import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
from settings import DB_PASSWORD, DB_USER ,DB_TEST_NAME


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = DB_TEST_NAME
        self.database_path = "postgres://{}:{}@{}/{}".format(DB_USER,DB_PASSWORD,'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
        self.new_question_test = {
            'question': 'What is the capital of France?',
            'answer': 'Paris',
            'category': '3',
            'difficulty': '1'
        }    
        self.searchTerm_test ={
            'searchTerm': 'movie'
        } 
        self.searchTerm_test_error ={
            'searchterm': 'movie'
        } 
        self.quiz_test = {
            'quiz_category': {'type': "History", 'id': 6},
            'previous_questions': [11, 23, 16],
        }
        self.quiz_test_error = {
            'quiz_category': {'type': "History", 'id': 1000},
            'previous_questions': [12, 15, 23],
        }
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['totalQuestions'])

    def test_404_sent_request_beyond_valid_page(self):
        res = self.client().get('/questions?page=1000',json={'rating':1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'resource not found')
    # get all categories test
    def test_get_all_categories(self):
        res = self.client().get('/categories')
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    def test_404_get_all_categories(self):
        for i in {0, 100}:
            res = self.client().get(f'/categories?page={i}')    
            data = res.get_json()
            self.assertEqual(res.status_code, 404)
            self.assertFalse(data['success'])
            self.assertTrue(data['message'])

    # get all questions test
    def test_get_all_questions(self):
        res = self.client().get('/questions')
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(data['categories'])

    def test_422_get_all_questions(self):
        for i in {0, 100}:
            res = self.client().get(f'/questions?page={i}')    
            data = res.get_json()
            self.assertEqual(res.status_code, 422)
            self.assertFalse(data['success'])
            self.assertTrue(data['message'])

    def test_404_get_all_questions(self):
        for i in {0, 100}:
            res = self.client().get(f'/questions?page={i}')    
            data = res.get_json()
            self.assertEqual(res.status_code, 404)
            self.assertFalse(data['success'])
            self.assertTrue(data['message'])        
    
    # delete question test
    def test_delete_question(self):
        question = Question.query.filter(Question.id == 9).one_or_none()
        res = self.client().delete('/questions/9')
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], f'Question {question} is deleted')

    def test_404_delete_questions(self):
        id = 1000 
        res = self.client().delete(f'/questions/{id}')
        data = res.get_json()
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])    
    
    # create new question test
    def test_create_new_question(self):
        res = self.client().post('/questions',json=self.new_question_test)
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['message'])

    def test_422_create_new_question(self):
        res = self.client().post('/questions',json=self.new_question_test)
        data = res.get_json()
        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertTrue(data['message'])
    
    # search a given question test 
    def test_search_question(self):
        res = self.client().post(f'/questions/search', json=self.searchTerm_test)
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertFalse(data['success'])
        self.assertTrue(data['message'])

    def test_400_search_question(self):
        res = self.client().post(f'/questions/search', json=self.searchTerm_test_error)
        data = res.get_json()
        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertTrue(data['message'])
    
    # get questions by category test
    def test_get_questions_by_category(self):
        res = self.client().get(f'/categories/5/questions')
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['totalQuestions'])    

    def test_404_get_questions_by_category(self):
        res = self.client().get(f'/categories/100/questions')
        data = res.get_json()
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertTrue(data['message'])
    
    # get quiz questions test
    def test_get_quiz_questions(self):
        res = self.client().post('/quizzes', json = self.quiz_test)
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertFalse(data['question'])

    def test_400_get_quiz_questions(self):     
        res = self.client().post('/quizzes', json = self.quiz_test_error)
        data = res.get_json()
        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertTrue(data['message'])

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()