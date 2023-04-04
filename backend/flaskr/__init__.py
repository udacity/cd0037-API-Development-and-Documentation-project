import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    with app.app_context():
        setup_db(app)

        """
        @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
        Use Flask-CORS to enable cross-domain requests and set response headers.
        """
        CORS(app, resources={r"/*": {"origins": "*"}})
        
        
        """
        @TODO: Use the after_request decorator to set Access-Control-Allow
        Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). 
        This endpoint should return a list of questions, number of total questions, current category, categories.
        """
        @app.after_request
        def after_request(response):
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
            response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
            return response        


        """
        @TODO:
        Create an endpoint to handle GET requests
        for all available categories.
        """
        @app.route('/categories')
        def get_categories():
            # get all category objects
            categories = Category.query.all()
            # create a dictionary with the category id as the key and the category type as the value
            formatted_categories = {category.id: category.type for category in categories}
            # return the dictionary as a json response
            return jsonify({
                'success': True,
                'categories': formatted_categories
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
        @app.route('/questions')
        def get_questions():
            page = request.args.get('page', 1, type=int)
            start = (page - 1) * QUESTIONS_PER_PAGE
            end = start + QUESTIONS_PER_PAGE
            questions = Question.query.all()
            formatted_questions = [question.format() for question in questions]
            categories = Category.query.all()
            formatted_categories = {category.id: category.type for category in categories}
            return jsonify({
                'success': True,
                'questions': formatted_questions[start:end],
                'total_questions': len(formatted_questions),
                'categories': formatted_categories,
                'current_category': None
            })
        

        """
        @TODO:
        Create an endpoint to DELETE question using a question ID.

        TEST: When you click the trash icon next to a question, the question will be removed.
        This removal will persist in the database and when you refresh the page.
        """
        @app.route('/questions/<int:question_id>', methods=['DELETE'])
        def delete_question(question_id):
            try:
                question = Question.query.get(question_id)
                question.delete()
                return jsonify({
                    'success': True,
                    'deleted': question_id
                })
            except:
                abort(422)

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
            new_question = body.get('question', None)
            new_answer = body.get('answer', None)
            new_category = body.get('category', None)
            new_difficulty = body.get('difficulty', None)
            try:
                question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
                question.insert()
                return jsonify({
                    'success': True,
                    'created': question.id
                })
            except:
                abort(422)


        """
        @TODO:
        Create a POST endpoint to get questions based on a search term.
        It should return any questions for whom the search term
        is a substring of the question.

        TEST: Search by any phrase. The questions list will update to include
        only question that include that string within their question.
        Try using the word "title" to start.
        """
        @app.route('/questions/search', methods=['POST'])
        def search_questions():
            body = request.get_json()
            search_term = body.get('searchTerm', None)
            questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
            formatted_questions = [question.format() for question in questions]
            return jsonify({
                'success': True,
                'questions': formatted_questions,
                'total_questions': len(formatted_questions),
                'current_category': None
            })
        

        """
        @TODO:
        Create a GET endpoint to get questions based on category.

        TEST: In the "List" tab / main screen, clicking on one of the
        categories in the left column will cause only questions of that
        category to be shown.
        """
        @app.route('/categories/<int:category_id>/questions')
        def get_questions_by_category(category_id):
            questions = Question.query.filter(Question.category == category_id).all()
            formatted_questions = [question.format() for question in questions]
            return jsonify({
                'success': True,
                'questions': formatted_questions,
                'total_questions': len(formatted_questions),
                'current_category': category_id
            })

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
        @app.route('/quizzes', methods=['POST'])
        def get_quiz_question():
            body = request.get_json()
            previous_questions = body.get('previous_questions', None)
            quiz_category = body.get('quiz_category', None)
            if quiz_category['id'] == 0:
                questions = Question.query.all()
            else:
                questions = Question.query.filter(Question.category == quiz_category['id']).all()
            formatted_questions = [question.format() for question in questions]
            def get_random_question():
                return formatted_questions[random.randint(0, len(formatted_questions) - 1)]
            question = get_random_question()
            while question['id'] in previous_questions:
                question = get_random_question()
            return jsonify({
                'success': True,
                'question': question
            })
        
        """
        @TODO:
        Create error handlers for all expected errors
        including 404 and 422.
        """
        @app.errorhandler(404)
        def not_found(error):
            return jsonify({
                'success': False,
                'error': 404,
                'message': 'Not found'
            }), 404

    return app


 

