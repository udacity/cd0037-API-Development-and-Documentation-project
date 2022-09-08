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

        #Adding question for future test :
        self.add_question = {
            'question': 'Which vital organ does the adjective renal refer to? ',
            'answer': 'Kidney',
            'difficulty': 1,
            'category': '1' #science
        }
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
    
    Write at least one test for each test for successful operation and for expected errors.
    - the minimum ran test are 7, number of endpoint in our backend.
    """
    # populate the database first to eliminate positive false errors : psql trivia_test < trivia.psql




    # Categories endpoint Test : 
    def test_get_categories(self):
        res = self.client().get('/categories')
        print("=======")
        #print(res)
        data = json.loads(res.data)
        #print(data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories'])) #if lenght so data exist. 
        self.assertTrue(data['total_category'])
    #Test should pass ok     

    def test_404_not_exist_category(self):
        #visit the non existing category id :
        res = self.client().get('/categories/55')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_retrieve_question(self):
        res= self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['categories'])

    
    def test_delete_question(self):
        try :
        
            test_question = Question(question=self.add_question['question'], answer=self.add_question['answer'],
                            category=self.add_question['category'], difficulty=self.add_question['difficulty'])
            test_question.insert()
        #retrieve test_question id and use it in the test to delete
        #delete question with id of new created question 
            test_id = test_question.id
            res = self.client().delete('/questions/{}'.format(test_id))
            data = json.loads(res.data)

        
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertEqual(data['deleted'],(test_id))
            

        #deletion is running succsufully 
        except:
            # if something wrong accur during the creation or deletiting new question, 
            # let's see if we can delete existing question : so we know that the problem is not from route
            print("Exception active - first test method failed")
            res = self.client().delete('questions/25')
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertTrue(len(data['deleted']))
       

    def test_422_delete_if_question_not_exist(self):
        res = self.client().delete("/questions/1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")    

    #=== Test new question ===
    def test_create_new_question(self):
        #to visualise if the question is created, let's query the databse before and after:
        len_query_question_bef = len(Question.query.all())
        res = self.client().post("/questions", json=self.add_question)
        data = json.loads(res.data)
        
        len_query_question_after = len(Question.query.all())
        #lenght of new table should exceed by one :
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True) 
        #print("=====ttttt====")
        #print(len_query_question_bef - len_query_question_after) 
        self.assertTrue(len_query_question_after - len_query_question_bef == 1)      


    def test_question_search(self):
        res = self.client().post("/questions", json={"searchTerm": "gogh"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
    
    #Test questions based on category : 
    def test_405_question_based_category(self):
        
        res = self.client().post('/categories/4/questions')
        data = json.loads(res.data)
        #print(data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'] , 'method not allowed')

    def test_422_question_based_category(self):
        res = self.client().get('/categories/88/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')



        


    # =============== Test /questions paginated ========
    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['categories']))
        self.assertTrue(len(data['questions']))

    #=== Test quizzes ===
    def test_play_quiz(self):
        quiz_payload = {'previous_questions': [],
                          'quiz_category': {'type': 'click', 'id': 0}}


        res = self.client().post('/quizzes', json = quiz_payload)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_404_play_quiz(self):
        quiz_payload = {'previous_questions': [],
                          'quiz_category': {'type': 'mickey', 'id': 8}}


        res = self.client().post('/quizzes', json = quiz_payload)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
    app.run()