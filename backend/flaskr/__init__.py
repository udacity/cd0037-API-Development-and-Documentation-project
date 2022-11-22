import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def null_or_blank(stringCheck):
    if stringCheck is None or stringCheck == "":
        return True
    return False

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
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
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route("/categories", methods=["GET"])
    def retrieve_categories():
        categories = Category.query.all()
        categoryMap = {}
        for category in categories:         # add categories to a map
            categoryMap[category.id] = category.type

        return jsonify(
            {
                "success": True,
                "categories": categoryMap,
                "total_categories": len(categoryMap)
            }
        )

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
    @app.route("/questions", methods=["GET"])
    def retrieve_questions():
        page = request.args.get("page", 1, type=int)
        print("page requested:" + str(page))
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        questions = Question.query.all()            # get list of questions
        questionsFormatted  = [question.format() for question in questions]          # format questions so that we can jsonfy it
        paginatedQuestions = questionsFormatted[start:end]          # only return paginated result
        
        categories = Category.query.all()           # get list of categories
        categoryMap = {}
        for category in categories:         # add categories to a map
            categoryMap[category.id] = category.type

        return jsonify({
            "success": True,
            "questions": paginatedQuestions,
            "total_questions": len(questionsFormatted),
            "categories": categoryMap,
            "current_category": None # current category empty, since there is no category for this endpoint
        })

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

            if question is None:
                abort(404)
            question.delete()
            questionsCount = Question.query.count()

            return jsonify({
                "success": True,
                "deleted": question_id,
                "total_questions": questionsCount

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
    @app.route("/questions", methods=["POST"])
    def create_question():
        body = request.get_json()

        answer_text = body.get("answer", None)
        question_text = body.get("question", None)
        category = body.get("category", None)
        difficulty = body.get("difficulty", None)

        if null_or_blank(question_text) or null_or_blank(answer_text) or null_or_blank(category) or null_or_blank(difficulty):
            print("missing request argument")
            abort(400)

        try:
            question = Question(question = question_text, answer=answer_text, category=category, difficulty=difficulty)
            question.insert()

            return jsonify(
                {
                    "success": True,
                    "created": question.id
                }
            )

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
        if null_or_blank(search_term):
            abort(400)
        print("search: "+search_term)
        query = Question.query.filter(Question.question.ilike('%' + search_term + '%'))

        questionsFormatted = [question.format() for question in query]          # format questions so that we can jsonfy it

        if len(questionsFormatted) == 0:
            abort(404) #questions not found

        response = {
            "success": True,
            "questions": questionsFormatted,
            "total_questions": len(questionsFormatted),
            "current_category": None,
        }
        return jsonify(response)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def retrieve_questions_by_category(category_id):
        if category_id is None:
            abort(400)
        print("category: " + str(category_id))
        query = Question.query.filter(Question.category==str(category_id))
        questions = [question.format() for question in query]
        response = {
            "count": query.count(),
            "questions": questions
        }
        return jsonify(response)


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

