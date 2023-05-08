import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_question(request, questions):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in questions]
    return questions[start:end]


def create_app(db_URI="", test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.app_context().push()
    if db_URI:
        setup_db(app, db_URI)
    else:
        setup_db(app)
    #CORS(app)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PATCH,POST,DELETE,OPTIONS"
        )
        return response


    """GET METHODS"""

    @app.route("/categories")
    def get_categories():
        '''
        Fetches all categories from database

        Request Arguments: None

        Returns: JSON object with categories
        '''
        selection = Category.query.order_by(Category.id).all()
        categories = {category.id:category.type for category in selection}

        if len(categories) == 0:
            abort(404)
        
        return jsonify(
            {
                "success": True,
                "categories": categories
            }
        )


    @app.route("/questions")
    def get_questions():
        '''
        Fetches all questions from database

        Request Arguments: page - integer

        Returns: JSON object with 10 paginated questions, \
          total_questions, categories, current_category
        '''
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_question(request, selection) 
        if len(current_questions) == 0:
            abort(404)


        categories = Category.query.order_by(Category.id).all()
        category_types = [{"id": category.id, "type": category.type} for category in categories]
        print("current_questions ->", current_questions)
        print("selection ->", selection)

        return jsonify(
            {
                "success": True,
                "questions": current_questions,
                "total_questions": len(selection),
                "categories": category_types,
                "current_category": "History"
            }
        )
    
    @app.route("/categories/<int:category_id>/questions")
    def get_questions_by_category(category_id):
        '''
        Fetches all questions based on category from database

        Request Arguments: id - integer

        Returns: JSON object with questions, \
            total_questions, current_category
        '''
        category = Category.query.filter_by(id=category_id).one_or_none()

        if category is None:
            abort(404)

        try:
            questions = Question.query.filter_by(category=category.id).all()
            current_questions = paginate_question(request, questions)
            return jsonify(
                {
                    "success": True,
                    "questions": current_questions,
                    "total_questions": len(questions),
                    "current_category": category.type,
                }
            )
        except:
            abort(400)


    """DELETE METHODS"""

    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        '''
        Deletes a question based on id

        Request Arguments: id - integer

        Returns: JSON object with deleted question id, \
            questions, total_questions
        '''
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

            if question is None:
                abort(404)
            
            question.delete()
            selection = Question.query.order_by(Question.id).all()
            current_question = paginate_question(request, selection)

            return jsonify(
                {
                    "success": True,
                    "deleted": question_id,
                    "questions": current_question,
                    "total_questions": len(Question.query.all()),
                }
            )
        
        except:
            abort(422)


    """POST METHODS"""

    @app.route("/questions", methods=["POST"])
    def create_question():
        '''
        Creates a new question

        Request Arguments: None

        Returns: JSON object with success, created, \
          questions, total_questions
        '''
        body = request.get_json()

        question = body.get("question", None)
        answer = body.get("answer", None)
        difficulty = body.get("difficulty", None)
        category = body.get("category", None)

        try:
            question = Question(question=question, answer=answer, difficulty=difficulty, category=category)
            question.insert()

            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_question(request, selection)

            return jsonify(
                {
                    "success": True,
                    "created": question.id,
                    "questions": current_questions,
                    "total_questions": len(Question.query.all()),
                }
            )
        except:
            abort(422)


    """SEARCH METHODS"""
    @app.route("/questions/search", methods=["POST"])
    def search_question():
        '''
        Fetches all questions from database based on search term

        Request Arguments: None

        Returns: JSON object with success, questions, \
            total_questions, current_category
        '''
        body = request.get_json()

        key_word = body.get('searchTerm', None)
        
        if key_word:
            selection = Question.query.filter(Question.question.ilike(f'%{key_word}%')).all()

            current_questions = paginate_question(request, selection)

            return jsonify({
                "success": True,
                "questions": current_questions,
                "total_questions": len(selection),
                "current_category": "History"
            })

    """GET QUIZ METHODS"""

    @app.route("/quizzes", methods=["POST"])
    def get_quiz():
        '''
        Fetches question from database to plat the quiz

        Request Arguments: None

        Returns: JSON object with success, question
        '''
        try:
            body = request.get_json()
            previous_questions: list = body.get("previous_questions", None)
            category = body.get("quiz_category", None)
            category_id = category["id"]


            if category_id != 0:
                questions_by_chosen_category = Question.query.filter_by(category=category_id).filter(Question.id.notin_((previous_questions))).all()
            else:
                questions_by_chosen_category = Question.query.filter(Question.id.notin_((previous_questions))).all()
            if len(questions_by_chosen_category) > 0:
                new_question = random.choice(questions_by_chosen_category).format()
            
            print("DEBUG -> ", questions_by_chosen_category)
            print("DEGUB -> ", new_question)
            return jsonify(
                {
                    "success": True,
                    "question": new_question
                }
            )
        except:
            abort(422)

    """
    ERROR HANDLING
    """
    @app.errorhandler(400)
    def invalid_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "invalid request"
        }), 400

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

    @app.errorhandler(405)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed",
        }), 405

    return app

