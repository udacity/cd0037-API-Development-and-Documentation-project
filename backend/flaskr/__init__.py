import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import logging
from logging import Formatter, FileHandler

from sqlalchemy import func

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    """
    Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    """
    Use the after_request decorator to set Access-Control-Allow
    """
    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    """
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route("/categories")
    def retrieve_categories():
        try:
            categories = Category.query.order_by(Category.id).all()
            formatted_categories = [category.format() for category in categories]
            if len(categories) == 0:
                abort(404)
            return jsonify(
                {
                    "success": True,
                    "categories": formatted_categories,
                    "total_categories": len(Category.query.all()),
                }
            )
        except Exception as e:
            if hasattr(e, 'code') and e.code == 404:
                abort(404)
            else:
                abort(422)

    """
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    @app.route("/questions")
    def retrieve_questions():
        try:
            categories = Category.query.order_by(Category.id).all()
            formatted_categories = [category.format() for category in categories]

            selection = Question.query.order_by(Question.id).all()
            page = request.args.get("page", 1, type=int)
            start = (page - 1) * QUESTIONS_PER_PAGE
            end = start + QUESTIONS_PER_PAGE

            questions = [question.format() for question in selection]
            current_questions = questions[start:end]

            if len(current_questions) == 0:
                abort(404)

            return jsonify(
                {
                    "success": True,
                    "questions": current_questions,
                    "current_category": formatted_categories[0],
                    "categories": formatted_categories,
                    "total_questions": len(selection),
                }
            )
        except Exception as e:
            if hasattr(e, 'code') and e.code == 404:
                abort(404)
            else:
                abort(422)

    """
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    @app.route("/questions/<question_id>", methods=["DELETE"])
    def delete_question(question_id):
        try:
            question_id = int(question_id)
            question = Question.query.filter(Question.id == question_id).one_or_none()
            if question is None:
                abort(404)
            question.delete()
            return jsonify(
                {
                    "success": True,
                    "deleted": question_id,
                }
            )
        except Exception as e:
            if hasattr(e, 'code') and e.code == 404:
                abort(404)
            else:
                abort(422)

    """
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route("/questions", methods=["POST"])
    def create_question():
        try:
            body = request.get_json()
            new_question = body.get("question", None)
            if new_question is None:
                abort(422)
            new_answer = body.get("answer", None)
            if new_answer is None:
                abort(422)
            new_difficulty = body.get("difficulty", None)
            if new_difficulty is None:
                abort(422)
            new_category = body.get("category", None)
            if new_category is None:
                abort(422)
            question_entity = Question(question=new_question, answer=new_answer, difficulty=new_difficulty, category=new_category)
            question_entity.insert()
            return jsonify(
                {
                    "success": True,
                    "question": question_entity.question,
                    "answer": question_entity.answer,
                    "difficulty": question_entity.difficulty,
                    "category": question_entity.category,
                    "id": question_entity.id
                }
            )
        except:
            abort(422)


    """
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        try:
            body = request.get_json()
            search_term = body.get("searchTerm", None)
            categories = Category.query.order_by(Category.id).all()
            formatted_categories = [category.format() for category in categories]
            results = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
            formatted_results = [question.format() for question in results]
            return jsonify(
                {
                    "success": True,
                    "questions": formatted_results,
                    "current_category": formatted_categories[0],
                    "total_questions": len(results),
                }
            )
        except:
            abort(422)


    """
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route("/categories/<category_id>/questions")
    def retrieve_questions_by_category_id(category_id):
        try:
            category_id = int(category_id)
            app.logger.debug("Retrieving for category id: '" + str(category_id)  + "'.")
            current_category = Category.query.filter(Category.id == category_id).one_or_none()
            categories_all = Category.query.order_by(Category.id).all()
            formatted_categories = [category.format() for category in categories_all]
            app.logger.debug("Total categories: '" + str(len(formatted_categories))  + "'.")
            if current_category is None:
                abort(404)
            questions_for_category = Question.query.filter(Question.category == category_id).all()
            app.logger.debug("Matched number of questions: '" + str(questions_for_category)  + "'.")
            formatted_questions = [question.format() for question in questions_for_category]
            return jsonify(
                {
                    "success": True,
                    "questions": formatted_questions,
                    "current_category": current_category.format(),
                    "categories": formatted_categories,
                    "total_questions": len(questions_for_category),
                }
            )
        except Exception as e:
            if hasattr(e, 'code') and e.code == 404:
                abort(404)
            else:
                abort(422)


    """
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        try:
            body = request.get_json()
            previous_questions = body.get("previous_questions")
            quiz_category = body.get("quiz_category")
            quiz_category_id = int(quiz_category['id'])
            if quiz_category_id > 0:
                currentQuestion = Question.query.filter(
                        Question.category == quiz_category_id, (~Question.id.in_(previous_questions))
                    ).order_by(func.random()).first()
            else:
                currentQuestion = Question.query.filter(
                        (~Question.id.in_(previous_questions))
                    ).order_by(func.random()).first()
            if currentQuestion is None:
                abort(404)
            return jsonify(
                {
                    "success": True,
                    "question": currentQuestion.format()
                }
            )
        except Exception as e:
            if hasattr(e, 'code') and e.code == 404:
                abort(404)
            else:
                abort(422)


    """
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "bad request"}), 400

    return app

