import os
from flask import Flask, request, abort, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from sqlalchemy import delete

from models import db, setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    if test_config is None:
        setup_db(app)
    else:
        database_path = test_config.get('SQLALCHEMY_DATABASE_URI')
        setup_db(app, database_path=database_path)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    #CORS(app, resources={r"*/api/*" : {origins: '*'}})

    CORS(app)

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
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
        # Implement pagination
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * 10
        end = start + 10

        categories = get_all_formatted_category()

        return jsonify({
            'success': True,
            'categories': categories[start:end],
            'total_categories': len(categories)
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
        # Implement pagination
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * 10
        end = start + 10

        categories = get_all_formatted_category()

        questions = Question.query.all()
        formatted_questions = [question.format() for question in questions]

        return jsonify({
            'success': True,
            'questions': formatted_questions[start:end],
            'total_questions': len(formatted_questions),
            'categories': categories
        })

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):
        id_question = int(id)

        try:
            question = Question.query.filter(Question.id == id_question).one_or_none()

            if question is None:
                handle_error(404, 'Error: question not found')

            db.session.delete(question)
            db.session.commit()
        except:
            handle_error(422, 'An error occurred!')

        return jsonify({
            'success': True,
            'message': "deleted successfully"
        })

        # return jsonify({
        #     'success': True,
        #     'deleted': id_question,
        #     'question': current_questions,
        #     'total_question': len(current_questions)
        # })

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
        new_difficulty = body.get('difficulty', None)
        new_category = body.get('category', None)

        try:
            question = Question(question=new_question, answer=new_answer, category=int(new_category), difficulty=int(new_difficulty))
            question.insert()
        except:
            handle_error(422, 'An error occurred!')
        
        return({
            'success': True,
            'message': 'Create successfully!'
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
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * 10
        end = start + 10

        body = request.get_json()
        key_word = body['searchTerm']
        questions = db.session.query(Question).filter(Question.question.ilike(f'%{key_word}%')).all()
        formatted_questions = [question.format() for question in questions]

        return jsonify({
            'success': True,
            'questions': formatted_questions[start:end],
            'total_questions': len(formatted_questions),
        })

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route("/categories/<int:id>/questions")
    def get_all_question(id):
        # Implement pagination
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * 10
        end = start + 10

        id_category = int(id)
        categories = Category.query.filter_by(id=id_category).all()
        formatted_categories = [category.format() for category in categories]
        questions = Question.query.filter_by(category=id_category).all()
        formatted_questions = [question.format() for question in questions]

        return jsonify({
            'success': True,
            'questions': formatted_questions[start:end],
            'total_questions': len(formatted_questions),
            'currentCategory': formatted_categories[0]
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
    @app.route("/quizzes", methods=['POST'])
    def get_question_to_play():
        data = request.get_json()
        previous_questions = data.get('previous_questions')
        quiz_category = data.get('quiz_category')
        result = None
        questions = []

        # get all questions
        if quiz_category['id'] is 0:
            questions = Question.query.all()
        else:
            questions = Question.query.filter_by(category=quiz_category['id']).all()

        format_questions =  [question.format() for question in questions]
        if len(format_questions) != 0:
            if len(previous_questions) is 0:
                result = format_questions[0]
            else:
                data = [question for question in format_questions if question['id'] not in previous_questions]
                if len(data) != 0:
                    result = data[0]

        return jsonify({
            'question': result
        })

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    def handle_error(code, message):
        error_message = ({'message': message})
        abort(Response(error_message, code))

    def get_all_formatted_category():
        categories = Category.query.all()
        formatted_categories = [category.format() for category in categories]
        return formatted_categories

    return app

