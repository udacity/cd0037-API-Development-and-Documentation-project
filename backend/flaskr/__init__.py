import os
from queue import Empty
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    """
    @DONE: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs [for example: I should allow this http://example.com:5000/api/v1/questions to be accepted as http://example.com:5000/questions]
    """
    cors = CORS(app, resources={r"/*": {"origins": "*"}})


    """
    @DONE: Use the after_request decorator to set Access-Control-Allow [done]
    """ 
    # CORS headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers', 
            'Content-Type, Authorization, true')
        response.headers.add(
            'Access-Control-Allow-Methods', 
            'GET, PUT, POST, PATCH, DELETE, OPTIONS')
        return response

    """
    @DONE:
    Create an endpoint to handle GET requests
    for all available categories. [done]
    """
    @app.route('/categories')
    def categories():
        # get all categories order by ID
        categories = Category.query.order_by(Category.id).all()

        # create a dictionary of all categories
        categories_dict = {}

        # make the its ID as the key and its type as the value for that element
        for category in categories:
            categories_dict[category.id] = category.type

        return jsonify({
            'categories': categories_dict,
        })

    """
    @DONE:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories. [done]

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions. [done]
    """
    @app.route('/questions')
    def get_questions():

        # get all questions order by ID
        selection = Question.query.order_by(Question.id).all()

        formatted_questions = paginate_questions(request, selection)

        if len(formatted_questions) == 0:
            abort(404)

        # get all categories order by ID
        categories = Category.query.order_by(Category.id).all()

        # create a dictionary of all categories
        categories_dict = {}

        # make the its ID as the key and its type as the value for that element
        for category in categories:
            categories_dict[category.id] = category.type

        return jsonify({
            'questions': formatted_questions,
            'total_questions': len(Question.query.all()),
            'categories': categories_dict,
            'current_category': None
        })

    """
    @DONE:
    Create an endpoint to DELETE question using a question ID. [done]

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page. [done]
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):

        try:
            # get the question with specific question ID
            question = Question.query.filter(Question.id == question_id).one_or_none()

            # delete the question
            question.delete()

        except:
            abort(422)

        return jsonify({
            'success': True,
            'deleted': question_id,
        })
    """
    @DONE:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score. [done below]

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab. [done]
    """

    """
    @DONE:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question. [done below]

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start. [done]
    """
    @app.route('/questions', methods=['POST'])
    def create_or_search_questions():

        body = request.get_json()

        # get the attributes of the question object
        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_category = body.get('category', None)
        new_difficulty = body.get('difficulty', None)

        # this will activie the search feature if it's found in the request body
        searchTerm = body.get('searchTerm', None)
        
        if searchTerm:

            # Case-insensitive and partial search for questions by title
            questions = Question.query.order_by(Question.id).filter(
                Question.question.ilike("%{}%".format(searchTerm))).all()

            # in case there's no result from the search
            if len(questions) == 0:
                    abort(404)

            # paginate the questions in groups of 10
            formatted_questions = paginate_questions(request, questions)

            return jsonify({
                'questions': formatted_questions,
                'total_questions': len(Question.query.all()),
                'current_category': None,
            })

        else:

            try:
                # create a new question object 
                question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)

                # insert it into the DB
                question.insert()

                return jsonify({
                    'success': True,
                    'created': question.format(),
                })
                
            except:
                abort(400)

    """
    @DONE:
    Create a GET endpoint to get questions based on category. [done]

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown. [done]
    """
    #==========================================================================
    @app.route('/categories/<int:id>/questions')
    def get_questions_by_category_id2(id):

        # get all questions with category ID equal to 'id' from the parameters of the func.
        selection = Question.query.filter(Question.category == id).order_by(Question.id).all()

        # paginate the questions in groups of 10
        current_questions = paginate_questions(request, selection)

        # get the category object with an ID equal to 'id from the parameters of the func.
        current_category = Category.query.filter(Category.id == id).one_or_none()

        if current_category is None:
            abort(404)

        # format the result to be accepted in jsonify return below
        current_category = current_category.format()

        return jsonify({
            'questions': current_questions,
            'total_questions': len(Question.query.all()),
            'current_category': current_category['type'],
        })

    #==========================================================================

    """
    @DONE:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions. [done]

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not. [done]
    """

    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        # get the request body
        body = request.get_json()

        previous_questions = body.get('previous_questions', None)
        quiz_category = body.get('quiz_category', None)

        # in case of All category
        if quiz_category['id'] == 0:
            # get all the questions which are not from the previous questions from all categories.
            questions_by_category = Question.query.order_by(Question.id).filter(
                Question.id.notin_(previous_questions)
            ).all()

        # in case of specific category
        else:
            # get all the questions order by ID that have the category 'new_category' from above AND their ID is not from the previous questions.
            questions_by_category = Question.query.order_by(Question.id).filter(
                Question.category == quiz_category['id'], Question.id.notin_(previous_questions)
            ).all()

        # in case there's questions to send. 
        if len(questions_by_category) > 0: 

            # choice a random question from the list
            random_question = random.choice(questions_by_category)

            return jsonify({
                'question': random_question.format(),
            })    

        # in case there isn't any question left to send.    
        else:
            return jsonify({
                'question': None,
            })    

    """
    @DONE:
    Create error handlers for all expected errors
    including 400, 404, 405, 422 and 500. [done]
    """
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'message': "resource not found",
            'error': 404,
        }), 404
    
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'message': "unprocessable",
            'error': 422,
        }), 422
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'message': "method not allowed",
            'error': 405,
        }), 405

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'message': "bad request",
            'error': 400,
        }), 400
    
    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'message': "internal server error",
            'error': 500,
        }), 500

    return app

