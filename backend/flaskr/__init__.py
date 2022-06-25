from nis import cat
import os
from unicodedata import category
from flask import Flask, request, abort, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, all_questions):
    """Separate questions into pages of 10 question per page"""
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    formatted_questions = [question.format() for question in all_questions]
    current_questions = formatted_questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app, resources={r"api/*": {"origin": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type, Authorization"
        )
        response.headers.add(
            "Access-Control-Headers", "GET, POST, PATCH, DELETE, OPTIONS"
        )
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """

    @app.route("/categories")
    def get_all_categories():
        try:
            categories = Category.query.all()
            formatted_categories = [category.format() for category in categories]

            # convert categories to dictionary
            categories_dictionary = {
                formatted_category["id"]: formatted_category["type"]
                for formatted_category in formatted_categories
            }

            if len(categories) is None:
                abort(404, "No category found")

            return jsonify({"success": True, "categories": categories_dictionary})
        except Exception as err:
            abort(err.code)

    @app.route("/questions")
    def get_paginated_questions():

        # get categories in json format from the above defined get_categories
        categories = get_all_categories().get_json()["categories"]

        all_questions = Question.query.order_by(Question.id).all()

        current_questions = paginate_questions(request, all_questions)

        # raise error if there is no question on the current page
        if len(current_questions) == 0:
            abort(404, "No questions on requested page")

        return jsonify(
            {
                "success": True,
                "questions": current_questions,
                "len_question": len(current_questions),
                "current_category": None,
                "categories": categories,
                "total_questions": len(all_questions),
            }
        )

    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_specific_question(question_id):
        question = Question.query.filter(Question.id == question_id).one_or_none()

        if not question:
            abort(404, f"Question with id: {question_id} does not exist")
        else:
            try:
                question.delete()

                current_questions = get_paginated_questions().get_json()["questions"]

                return jsonify(
                    {
                        "success": True,
                        "deleted": question_id,
                        "questions": current_questions,
                        "total_questions": len(Question.query.all()),
                    }
                )
            except Exception as err:
                abort(err.code)

    @app.route("/questions", methods=["POST"])
    def post_new_question():

        body = request.get_json()

        # define the components of the question
        qst_details = {
            "new_question": body.get("question", None),
            "new_answer": body.get("answer", None),
            "new_category": body.get("category", None),
            "new_difficulty": body.get("difficulty", None),
        }

        # raise error if any parameter is missing
        for detail in qst_details:
            if not qst_details[detail]:
                abort(400, "A detail of the new question is not defined")

            else:
                question = Question(
                    question=qst_details["new_question"],
                    answer=qst_details["new_answer"],
                    category=qst_details["new_category"],
                    difficulty=qst_details["new_difficulty"],
                )

        try:

            question.insert()

            all_questions = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, all_questions)
            return jsonify(
                {
                    "success": True,
                    "created": question.id,
                    "questions": current_questions,
                    "total_questions": len(question.query.all()),
                }
            )

        except Exception as err:
            abort(err.code)

    @app.route("/questions/results", methods=["POST"])
    def search_questions():

        body = request.get_json()
        search_term = body.get("searchTerm")

        if search_term is None:

            abort(400, "Search term is undefined")

        else:
            try:
                categories = get_all_categories().get_json()["categories"]

                result_query = Question.query.filter(
                    Question.question.ilike(f"%{search_term}%")
                ).all()

                questions = [question.format() for question in result_query]

                return jsonify(
                    {
                        "success": True,
                        "questions": questions,
                        "total_questions": len(result_query),
                        "categories": categories,
                        "current_category": None,
                    }
                )

            except Exception as err:
                abort(err.code)

    @app.route("/categories/<int:category_id>/questions")
    def get_questions_by_category(category_id):

        current_category_query = Category.query.get(category_id)

        # abort if there is no such category
        if not current_category_query:
            abort(404, "Selected category does not exist")

        else:
            try:
                current_category = current_category_query.type

                categorized_questions_query = Question.query.filter(
                    Question.category == category_id
                )

                categorized_questions = [
                    question.format() for question in categorized_questions_query
                ]
                total_questions = len(categorized_questions)

                return jsonify(
                    {
                        "success": True,
                        "questions": categorized_questions,
                        "current_category": current_category,
                        "total_questions": total_questions,
                    }
                )
            except Exception as err:
                abort(err.code)

    @app.route("/quizzes", methods=["POST"])
    def get_quiz_questions():
        body = request.get_json()

        category = body.get("quiz_category")["id"]

        if category is None:
            abort(400, "Invalid category selected")

        else:
            category_id = int(category)

            previous_questions = body.get("previous_questions", None)
            try:
                if category_id == 0:
                    # get all questions
                    categorized_questions = get_paginated_questions().get_json()[
                        "questions"
                    ]
                    if len(previous_questions) < 5:
                        question = random.choice(
                            [
                                qst
                                for qst in categorized_questions
                                if qst["id"] not in previous_questions
                            ]
                        )
                    else:
                        question = None

                else:
                    # get categorized question
                    categorized_questions = get_questions_by_category(
                        category_id
                    ).get_json()["questions"]
                    if len(previous_questions) < len(categorized_questions):
                        question = random.choice(
                            [
                                qst
                                for qst in categorized_questions
                                if qst["id"] not in previous_questions
                            ]
                        )
                    else:
                        question = None

                return jsonify(
                    {
                        "success": True,
                        "question": question,
                        "previous_questions": previous_questions,
                    }
                )
            except Exception as err:
                abort(400)

    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify(
                {
                    "success": False,
                    "error": 400,
                    "message": f"bad request : {error.description}",
                }
            ),
            400,
        )

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify(
                {
                    "success": False,
                    "error": 404,
                    "message": f"resource not found : {error.description}",
                }
            ),
            404,
        )

    @app.errorhandler(405)
    def not_allowed(error):
        return (
            jsonify(
                {
                    "success": False,
                    "error": 405,
                    "message": f"method not allowed : {error.description}",
                }
            ),
            405,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify(
                {
                    "success": False,
                    "error": 422,
                    "message": f"unprocessable : {error.description}",
                }
            ),
            422,
        )

    return app
