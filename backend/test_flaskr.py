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
        self.database_path = "postgres://{}/{}".format('student:student@localhost:5432', self.database_name)
        # new question test
        self.new_question ={
            'id':25,
            'question':'test question',
            'answer': 'test answer',
            'difficulty':3,
            'category':1
        }
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
    
    # test for retrieving all categories
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertEqual(data['categories'])
        self.assertEqual(len(data['categories']),6)
        self.assertEqual(data['categories'], dict)
    # retrieve all questions
    def test_get_questions(self):
        res = self.client().get('/questions')
        data= json.loads(res.data)
        # status code
        self.assertEqual(res.status_code,200)  
        self.assertEqual(data['success'],True)
        #questions
        self.assertEqual(data['questions'])
        self.assertIsInstance(data['questions'],list)
        self.assertEqual(len(data['questions']),10)
        # total questions
        self.assertEqual(data['total_questions'],19)
        # categories  
        self.assertEqual(data['categories'])
        self.assertEqual(len(data['categories']),6)
        self.assertEqual(data['categories'],dict)
        self.assertEqual(data['current_category'], None)
    # create question test
    def test_create_question(self):
        res = self.client().post('\questions', json=self.new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertEqual(data['created'],25)
    # delete question test
    def test_delete_questions(self):
        res = self.client().delete('/questions/25')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertEqual(data['deleted'],25)
    # 404 delete question error test
    def test_404_delete_not_valid_question(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'resource not found')
    # search question test
    def test_search_question(self):
        res = self.client().post('/search',json={'searchTerm': 'Taj Mahal'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertEqual(data['questions'])
        self.assertIsInstance(data['questions'],list)
        self.assertEqual(data['questions'],1)
        self.assertEqual(data['total_questions'],1)
        self.assertEqual(data['current_category'],None)
    # search question without results
    def test_search_question_without_results(self):
        res = self.client().post('/search',json={'searchTerm': 'xxxx'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertEqual(data['questions'])
        self.assertIsInstance(data['questions'],list)
        self.assertEqual(data['questions'],0)
        self.assertEqual(data['total_questions'],0)
        self.assertEqual(data['current_category'],None)
    # get questions by category test
    def test_get_questions_by_category(self):
        res = self.client().get('/categories/1/questions?page=1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['questions'],list)
        self.assertEqual(len(data['questions']),3)
        self.assertEqual(data['total_questions'],3)
        self.assertEqual(data['current_category'],1)
    # 404 questions without category test
    def test_404_get_questions_by_category(self):
        res = self.client().get('/categories/1000/questions?page=1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'resource not found')





# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()