import os
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page =  request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    formatted_questions = questions[start:end]

    return formatted_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    
    """
   To set up CORS. Allow '*' for origins.
    """
    CORS(app)

    """
    To set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    # To handle GET requests for questions
    @app.route('/categories', methods=['GET'])
    def get_categories():
        # To query all available categories
        selection = Category.query.order_by(Category.id).all()
        categories = paginate_questions(request, selection)

        if len(categories) == 0:
            abort(404)

        return jsonify(
            {
                'success': True,
                'categories': {category.id: category.type for category in selection},
                'total_categories': len(Category.query.all()),
            }
        )
    
    # To handle GET requests for questions
    @app.route('/questions', methods=['GET'])
    def get_questions():
        selection = Question.query.order_by(Question.id).all()
        formatted_questions = paginate_questions(request, selection)
        category = Category.query.all()

        if len(formatted_questions) == 0:
            abort(404)

        # To return a list of questions, number of total questions, current category and categories
        return jsonify(
            {
                'success': True,
                'questions': formatted_questions,
                'total_questions': len(selection),
                'current_category': [],
                'categories': {category.id:category.type for category in category}
            }
        )

    # To DELETE question using a question ID
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        try:
            # To get a question by id
            question = Question.query.filter(Question.id == question_id).one_or_none()
            if question is None:
                abort(404)
            # To delete the question of the selected id
            question.delete()

            return jsonify(
                {
                    'success': True,
                    'deleted': question_id,
                }
            )
        
        except:
            abort(422)
   
    # To POST a new question, which will require the question and answer text, category, and difficulty score
    @app.route("/questions", methods=["POST"])
    def create_question():
        body = request.get_json()

        # To initialize the new question paramiters
        new_question = body.get("question", None)
        new_answer = body.get("answer", None)
        new_category = body.get("category", None)
        new_difficulty = body.get("difficulty", None)

        try:
            # To create the new record
            question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
            question.insert()

            return jsonify(
                {
                    "success": True,
                    "created": question.id,
                    "total_questions": len(Question.query.all()),
                }
            )

        except:
            abort(422)

    # To get questions based on a search term
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        body = request.get_json()
        search_term = body.get('search_term', '')
        results = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
        data = []
        for result in results:
            data.append({
                'id': result.id,
                'question': result.question,
                'answer': result.answer
            })
       
        response = paginate_questions(request, results)

        return jsonify(
            {
                "success": True,
                "questions": response,
                "total_questions": len('questions')
            }
        )
    # To get questions based on a search term
    @app.route("/categories/<int:id>/questions", methods=["GET"])
    def get_questions_by_category(id):
        # To get category by id
        category = Category.query.filter_by(id=id).one_or_none()

        try:
            # To query questions from the selected category
            selection = Question.query.filter_by(category=category.id).all()
            formatted_questions = paginate_questions(request, selection)

            return jsonify(
                {
                    "success": True,
                    "questions": formatted_questions,
                    "current_category": category.type,
                    "total_questions": len(formatted_questions)
                }
            )
        except:
            abort(400)

    # To get questions to play the quiz
    @app.route("/quizzes", methods=["POST"])
    def play_quiz():
        try:
            body = request.get_json()
            previous_questions = body.get('previous_questions', None)
            quiz_category = body.get('quiz_category', None)
            quiz_category_id = quiz_category['id']

            # To load random questions from all categories if 'ALL' is selected
            if quiz_category_id == 0:
                questions = Question.query.filter(Question.id.notin_(previous_questions)).all()

            #  To load questions by category and query questions not in previous_questions list
            else:
                questions = Question.query.filter(Question.id.notin_(previous_questions), Question.category == quiz_category_id).all()
                
            #  To display random question that has not been displayed previously
            question = []
            if(len(questions)>0):
                question = random.choice(questions)
                question = question.format()
            else:
                question = None

            return jsonify({
                'success': True,
                'question': question
            })

        except Exception:
            abort(400)

    # Error handlers for all expected errors
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(405)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405
    
    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500

    return app

