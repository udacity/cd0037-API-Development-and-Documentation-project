import os
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category


# Categories
def get_categories_func():
    categories = Category.query.order_by(Category.id).all()
    category_obj={}
    for category in categories:
        category_obj[category.id] = category.type
    return category_obj


# Pagination

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start =  (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    books = [question.format() for question in selection]
    current_questions = books[start:end]

    return current_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={r"*": {"origins": "*"}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
      response.headers.add("Access-Control-Allow-Headers","Content-Type,Authorization,true")  
      response.headers.add("Access-Control-Allow-Methods", "POST,GET,PUT,DELETE,OPTIONS")
      return response
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories', methods = ['GET'])
    def get_categories():
        categories = get_categories_func()

        return jsonify({
            'success':True,
            'categories': categories
        })

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions', methods=['GET'])
    def get_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)
        categories = get_categories_func()
        if len(current_questions) == 0:
            abort(404)
        else:
            return jsonify({
                'success': True,
                'categories': categories, 
                'total_questions': len(Question.query.all()),
                'questions':current_questions,
            })


    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.get(question_id)

        if question is not None:
            question.delete()
            
            return jsonify({
                'success':True
            })
        else:
            abort(404)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()
        new_question = body.get('question',None)
        new_answer = body.get('answer',None)
        new_difficult = body.get('difficulty',None)
        new_category = body.get('category', None)

        add_question = Question(
            question = new_question, 
            answer = new_answer,
            difficulty= new_difficult,
            category= new_category
        )

        add_question.insert()

        return jsonify({
            'success':True
        })
        
    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_foubd(error):
        return jsonify({
            'success': False,
            "error": 404,
            "message": "Not found"
        }), 404

    @app.errorhandler(405)
    def not_foubd(error):
        return jsonify({
            'success': False,
            "error": 405,
            "message": "Method Not Allowed"
        }), 405

    return app

