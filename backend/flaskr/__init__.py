import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app)
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET, PUT, POST, DELETE, OPTIONS"
        )
        return response

    QUESTIONS_PER_PAGE = 10
    def paginated_questions(request, selection):
        page = request.args.get("page", 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        questions = [questions.format() for questions in selection]
        questions_on_page = questions[start:end]

        return questions_on_page
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route("/categories")
    def get_categories():
        if request.method != 'GET':
            abort(405)
        else:
            selection = Category.query.all()
            categories = {category.id: category.type for category in selection}

            if len(categories) == 0:
                abort(404)    

            return jsonify({"success": True, "categories": categories})

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
    @app.route("/questions")
    def get_questions():
        if request.method != 'GET':
            abort(405)
        else:
            selection = Question.query.order_by(Question.id).all()
            questions_on_page = paginated_questions(request, selection)
            get_categories = Category.query.all()
            categories = {category.id: category.type for category in get_categories}

            if len(questions_on_page) == 0:
                abort(404)
            
            return jsonify(
                {
                    "success": True,
                    "questions": questions_on_page,
                    "total_questions": len(Question.query.all()),
                    "categories": categories,
                    "current_category": True,
                }
            )
            
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
            selection = Question.query.order_by(Question.id).all()
            questions_list = paginated_questions(request, selection)

            return jsonify(
                {
                    "success": True,
                    "deleted": question_id,
                    "questions": questions_list,
                    "total_questions": len(Question.query.all()),
                }
            )

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
    def create_question_search_questions():
        if request.method != 'POST':
            abort(405)
        else:
            body = request.get_json()

            new_question = body.get("question", None)
            new_answer = body.get("answer", None)
            new_difficulty = body.get("difficulty", None)
            new_category = body.get("category", None)
            search = body.get("searchTerm", None)

            try:
                if search:
                    selection = Question.query.order_by(Question.id).filter(
                        Question.question.ilike("%{}%".format(search))
                    )
                    current_questions = paginated_questions(request, selection)

                    return jsonify(
                        {
                            "success": True,
                            "questions": current_questions,
                            "total_questions": len(selection.all()),
                        }
                    )
                else:
                    question = Question(
                        question=new_question,
                        answer=new_answer,
                        difficulty=new_difficulty,
                        category=new_category,
                    )
                    question.insert()

                    selection = Question.query.order_by(Question.id).all()
                    current_questions = paginated_questions(request, selection)

                    return jsonify(
                        {
                            "success": True,
                            "questions": current_questions,
                            "created": question.id,
                            "total_questions": len(Question.query.all()),
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
    # @app.route("/questions/search", methods=["POST"])
    # def search_questions():
    #     body = request.get_json()

    #     search = body.get("searchTerm", None)

    #     try:
    #         selection = Question.query.order_by(Question.id).filter(Question.question.ilike('{}'.format(search))).all()

    #         search_result = paginated_questions(request, selection)

    #         return jsonify(
    #             {
    #                 "success": True,
    #                 "questions": search_result,
    #                 "total_questions": len(selection),
    #                 "current_category": None,
    #             }
    #         )

    #     except:
    #         abort(422)
    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route("/categories/<category_id>/questions")
    def get_questions_by_category(category_id):
        if request.method != 'GET':
            abort(405)
        else:
            category = Category.query.filter(Category.id == category_id).one_or_none()

            if category is None:
                abort(404)

            selection = (Question.query.filter(Question.category == category_id).order_by(Question.id).all())
            questions_on_page = paginated_questions(request, selection)

            if len(questions_on_page) == 0:
                abort(404)

            return jsonify(
                {
                    "success": True,
                    "questions": questions_on_page,
                    "total_questions": len(Question.query.filter(Question.category == category_id).all()),
                    "current_category": category.type,
                }
            )
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
    @app.route("/quizzes", methods=["POST"])
    def create_quiz_questions():
        try:
            body = request.get_json()

            previous_questions = body.get("previous_questions", None)
            quiz_category = body.get("quiz_category", None)

            selection = Question.query.filter(~Question.id.in_(previous_questions))

            if "id" in quiz_category:
                category = quiz_category["id"]
                if category:
                    selection = selection.filter(Question.category == category)

            selection = selection.all()
            question = None

            if len(selection):
                question = random.choice(selection)

            return jsonify(
                {
                    "success": True,
                    "question": question.format() if question else question,
                }
            )

        except:
            abort(422)
    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(400)
    def bad_request(error):
        return (jsonify({"success": False, "error": 400, "message": "Bad request"}), 400)
    
    @app.errorhandler(404)
    def resource_not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "Resource not found"}),
            404,
        )

    @app.errorhandler(405)
    def not_allowed(error):
        return (
            jsonify({"success": False, "error": 405, "message": "Method not allowed"}),
            405,
        )
    @app.errorhandler(408)
    def request_timeout(error):
        return (jsonify({"success": False, "error": 408, "message": "Request timeout"}), 408)

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "Unprocessable"}),
            422,
        )
    return app

