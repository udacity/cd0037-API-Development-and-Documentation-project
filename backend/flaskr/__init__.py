import os
from flask import Flask, request, abort, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={r"/*": {"origins": "*"}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """

    @app.after_request
    def after_request(response: Response) -> Response:
        """Define headers for CORS"""
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories', methods=['GET'])
    def get_categories():
        """Get all the categories and return them in JSON format"""
        categories = Category.query.order_by(Category.type).all()

        categories_dict = {category.id: category.type for category in categories}

        if len(categories_dict) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'categories': categories_dict,
            'number_of_categories': len(categories_dict)
        })

    @app.route('/questions/<int:id>', methods=['GET'])
    def get_question(id):
        """Get a single question and return it in JSON format"""
        question = Question.query.get(id)

        if question is None:
            abort(404)

        return jsonify({
            'id': question.id,
            'question': question.question,
            'answer': question.answer,
            'category': question.category,
            'difficulty': question.difficulty
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
        page = request.args.get('page', 1, type=int)  # Default to page 1 if not specified
        start = (page - 1) * 10
        end = start + 10

        questions = Question.query.all()
        formatted_questions = [question.format() for question in questions]

        categories = Category.query.all()
        formatted_categories = {category.id: category.type for category in categories}

        return jsonify({
            'success': True,
            'questions': formatted_questions[start:end],
            'total_questions': len(formatted_questions),
            'categories': formatted_categories,
            'current_category': None  # or set appropriately if you have this information
        }), 200


    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):
        """Delete a question by id"""
        delete_question = Question.query.get(id)
        if delete_question is None:
            abort(404)

        delete_question.delete()
        return jsonify({
            'success': True,
            'question_id': delete_question.id
        })

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
        """Create a new question"""
        try:
            # Attempt to parse the JSON data from the request
            data = request.get_json()

            # Validate the data (optional but recommended)
            if 'question' not in data or 'answer' not in data or 'category' not in data or 'difficulty' not in data:
                abort(400, description="Missing data for the new question")

            # Create a new question object
            question = Question(question=data['question'], answer=data['answer'], category=data['category'],
                                difficulty=data['difficulty'])

            # Insert the new question into the database
            question.insert()

            # Return a success response with status code 201
            return jsonify({
                'success': True,
                'question': question.format(),
                'question_id': question.id
            }), 201

        except Exception as e:
            # Log the exception for debugging purposes
            print(f"Error: {e}")

            # Return a server error response with status code 500
            return jsonify({
                'success': False,
                'error': "An error occurred while processing the request"
            }), 500


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
        """Search for questions based on a search term"""
        data = request.get_json()
        search_term = data.get('searchTerm', None)

        if search_term:
            search_results = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
            formatted_questions = [question.format() for question in search_results]

            return jsonify({
                'success': True,
                'questions': formatted_questions,
                'total_questions': len(formatted_questions)
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No search term provided'
            }), 400

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        """Get questions by category"""
        try:
            questions = Question.query.filter_by(category=str(category_id)).all()
            formatted_questions = [question.format() for question in questions]
            if len(formatted_questions) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'questions': formatted_questions,
                'total_questions': len(formatted_questions),
                'current_category': category_id
            }), 200
        except Exception as e:
            abort(404)  # Assuming category not found or other errors

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
        """Get a random question for the quiz"""
        try:
            data = request.get_json()
            previous_questions = data.get('previous_questions', [])
            quiz_category = data.get('quiz_category', None)

            if quiz_category:
                category_id = quiz_category['id']
                if category_id == 0:  # Assuming '0' means 'All' categories
                    questions_query = Question.query.filter(Question.id.notin_(previous_questions))
                else:
                    questions_query = Question.query.filter_by(category=str(category_id)).filter(
                        Question.id.notin_(previous_questions))
            else:
                questions_query = Question.query.filter(Question.id.notin_(previous_questions))

            available_questions = questions_query.all()
            if available_questions:
                next_question = random.choice(available_questions).format()
            else:
                next_question = None

            return jsonify({
                'success': True,
                'question': next_question
            }), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'error': 'An error occurred while processing the request'
            }), 500

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
            'message': 'Resource not found'
            }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable'
            }), 422

    return app

