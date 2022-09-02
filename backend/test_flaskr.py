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
        self.database_path = "postgresql://{}:{}@{}/{}".format('postgres','password','localhost:5432', self.database_name)
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
    def test_retrieve_questions(self):
        """Test that retrieve questions endpoint runs as expected"""
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["questions"]))
    
    def test_404_when_page_not_exist(self):
        """Test that pagination works correctly- 
        that 404 error when a page is beyond valid range """
        res = self.client().get("/questions?page=300")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")
    
    def test_success_delete_question(self):
        """Test that we are able to delete a question"""
        res = self.client().delete("/questions/5")
        data = json.loads(res.data)
        question = Question.query.get(5)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], 5)
        self.assertEqual(question,None)
             


    def test_405_for_deleting_wrong_resource(self):
        """ Test we get a 405 when trying to delete the questions collection"""
        res = self.client().delete("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")
    
    def test_422_if_book_does_not_exist(self):
        res = self.client().delete("/questions/40")
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")
    
    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["categories"])



    def test_create_question(self):
        res = self.client().post("/questions",headers={"Content-Type": "application/json"},json={"question":"Who run's the world?","answer":"Girls","category":"1","difficulty":"4"})
        data = json.loads(res.data)
        question = Question.query.filter(Question.id == data["created"]).all()
        q= [i.format() for i in question]

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["created"], q[0]['id'])
    
    def test_405_if_book_creation_not_allowed(self):
        """Test to see if we get 405 error if we try post method to wrong endpoint"""
        res = self.client().post("/questions/28",json={"question":"how many hours in a day?","answer":"24","category":"1","difficulty":"4"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")

        
    def test_search_question(self):
        res = self.client().post("/questions/search",headers={"Content-Type":"application/json"},json={"searchTterm":"title"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        

    def test_play_quiz(self):
        res = self.client().post("/quizzes",headers={"Content-Type": "application/json"},json={"previous_questions": [1, 4, 20, 15],"quiz_category": {'type': 'History', 'id': '4'}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"])
    
    def test_filter_by_category(self):
        res = self.client().get("/categories/4/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertTrue(data["questions"])

    def test_400_search_question_with_empty_req_body(self):
        
        res = self.client().post("/questions/search",headers={"Content-Type":"application/json"})
        data = json.loads(res.data)
 

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "bad request")





      
        
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()