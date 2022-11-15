import random

from flask import Flask, jsonify, request
from flask_cors import CORS
from models import Category, Question, setup_db

QUESTIONS_PER_PAGE = 10

# questions pagination helper function


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
    # Solves working outside of app context error introduced by upgrading to newer versions of Flask
    # https://stackoverflow.com/questions/34122949/working-outside-of-application-context-flask
    app.app_context().push()
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type, Authorization"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET, POST, PATCH, DELETE, OPTIONS"
        )
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route("/categories")
    def get_categories():
        try:
            categories = Category.query.all()
            formatted_categories = {
                category.id: category.type for category in categories}
            # abort 404 if no categories found
            if len(formatted_categories) == 0:
                return not_found(404)

            return jsonify(
                {
                    "success": True,
                    "categories": formatted_categories,
                    "total_categories": len(categories),
                }
            )
        except Exception as e:
            return unprocessable(e)

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
        try:
            question = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, question)

            categories = Category.query.order_by(Category.id).all()
            categories_dict = {
                category.id: category.type for category in categories}

            if len(current_questions) == 0:
                return not_found(404)

            return jsonify(
                {
                    "success": True,
                    "questions": current_questions,
                    "total_questions": len(question),
                    "categories": categories_dict,
                    "current_category": None,
                }
            )
        except Exception as e:
            return unprocessable(e)

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()

            if question is None:
                return not_found(404)

            question.delete()

            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            return jsonify(
                {
                    "success": True,
                    "deleted": question_id,
                    "questions": current_questions,
                    "total_questions": len(Question.query.all())
                }
            ), 200

        except Exception as e:
            return unprocessable(e)

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

        new_question = body.get("question", None)
        new_answer = body.get("answer", None)
        new_difficulty = body.get("difficulty", None)
        new_category = body.get("category", None)

        try:
            question = Question(
                question=new_question,
                answer=new_answer,
                difficulty=new_difficulty,
                category=new_category,
            )
            question.insert()

            questions = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, questions)

            return jsonify(
                {
                    "success": True,
                    "created": question.id,
                    "questions": current_questions,
                    "total_questions": len(Question.query.all()),
                }
            ), 201  # rather status code 201 - created than just ok

        except Exception as e:
            return unprocessable(e)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route("/questions/search", methods=["POST"])
    def search_questions():
        body = request.get_json()
        search_term = body.get("searchTerm", None)
        # code enables search by category (QuestionView component modified already)
        search_category = None  # body.get("searchCategory", None)

        try:
            if search_category != None:
                results = Question.query.order_by(Question.id).filter(
                    Question.question.ilike(f"%{search_term}%"),
                    Question.category == search_category
                )
            else:
                results = Question.query.order_by(Question.id).filter(
                    Question.question.ilike(f"%{search_term}%")
                )

            current_questions = paginate_questions(request, results)

            # handle 404 error if no questions found
            if len(current_questions) == 0:
                return not_found(404)

            return jsonify(
                {
                    "success": True,
                    "questions": current_questions,
                    "total_questions": len(results.all()),
                    "current_category": None,
                }
            )

        except Exception as e:
            return unprocessable(e)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route("/categories/<int:category_id>/questions")
    def get_questions_by_category(category_id):
        try:
            results = Question.query.filter(
                Question.category == str(category_id)
            ).all()
            current_questions = paginate_questions(request, results)

            # handle 404 error if no questions found
            if len(results) == 0:
                return not_found(404)

            return jsonify(
                {
                    "success": True,
                    "questions": current_questions,
                    "total_questions": len(results),
                    "current_category": category_id,
                }
            )

        except Exception as e:
            return unprocessable(e)

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
    def play_quiz():
        body = request.get_json()
        previous_questions = body.get("previous_questions", None)
        quiz_category = body.get("quiz_category", None)

        try:
            if quiz_category["id"] == 0:
                questions = Question.query.all()
            else:
                questions = Question.query.filter(
                    Question.category == quiz_category["id"]
                ).all()

            # if no questions found
            if len(questions) == 0:
                return not_found(404)

            def get_random_question():
                return questions[random.randint(0, len(questions) - 1)]

            question = get_random_question()

            while question.id in previous_questions:
                question = get_random_question()

            return jsonify(
                {
                    "success": True,
                    "question": question.format(),
                }
            )

        except Exception as e:
            return unprocessable(e)

    # """
    # @BONUS:
    # Create an endpoint to POST a new category,
    # which will require the category and answer text,
    # category, and difficulty score.

    # TEST: When you submit a category on the "Add" tab,
    # the form will clear and the category will appear at the end of the last page
    # of the categorys list in the "List" tab.
    # """
    # @app.route("/categories", methods=["POST"])
    # def create_category():
    #     body = request.get_json()

    #     new_type = body.get("type", None)
    #     try:
    #         print(new_type)
    #         category = Category(type=new_type)
    #         category.insert()

    #         categories = Category.query.order_by(Category.id).all()

    #         return jsonify(
    #             {
    #                 "success": True,
    #                 "created": category.id,
    #                 "categories": [categories.format() for categories in categories],
    #                 "total_categories": len(Category.query.all()),
    #             }
    #         ), 201  # rather status code 201 - created than just ok

    #     except Exception as e:
    #         print(e)
    #         return unprocessable(e)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify(
            {
                "success": False,
                "error": 400,
                "message": "bad request",
            }
        ), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify(
            {
                "success": False,
                "error": 404,
                "message": "resource not found",
            }
        ), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify(
            {
                "success": False,
                "error": 422,
                "message": "unprocessable",
            }
        ), 422

    if __name__ == "__main__":
        app.run(debug=True)

    return app
