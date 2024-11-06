import os
import unittest
import json
from flaskr import create_app
from models import db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.database_name = "trivia_test"
        self.database_user = "Emmanuel"
        self.database_password = "Manos"
        self.database_host = "localhost:5432"
        self.database_path = f"postgresql://{self.database_user}:{self.database_password}@{self.database_host}/{self.database_name}"

        # Create app with the test configuration
        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": self.database_path,
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "TESTING": True
        })
        self.client = self.app.test_client

        # Bind the app to the current context and create all tables
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        """Executed after each test"""
        with self.app.app_context():
            db.session.remove()
            #db.drop_all()

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    # def test_get_categories(self):
    #     res = self.client().get("/categories")        
    #     data = json.loads(res.data)
    #     print(f'Data:{res.data}')
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertTrue(data["total_category"])
    #     self.assertTrue(len(data["categories"]))
    
    # def test_404_sent_requesting_beyond_valid_page(self):
    #     res = self.client().get("/categories?page=1000", json={"category": 1})
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data["success"], False)
    #     self.assertEqual(data["message"], "resource not found")

    def test_get_questions_category(self):
        res = self.client().get("/questions", json={"category": 1})    
        print(f'Data:{res.data}')   
        data = json.loads(res.data)
        print(f'Data:{data}')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["totalQuestion"])
        self.assertTrue(data["currentCategory"])
        self.assertTrue(len(data["questions"]))

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
