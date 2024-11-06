from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
        page = request.args.get("page", 1, type=int)
        print(f'page_num:{page}' )
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        questions = [question.format() for question in selection]
        current_questions = questions[start:end]

        return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    if test_config is None:
        setup_db(app)
    else:
        database_path = test_config.get('SQLALCHEMY_DATABASE_URI')
        setup_db(app, database_path=database_path)

    CORS(app)
    with app.app_context():
        db.create_all()

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
    for all available categories
    """
    @app.route("/categories")
    def retrieve_categories():
        selection = Category.query.order_by(Category.id).all()
        #current_categories = paginate_questions(request, selection)
        formatted_category = [category.format() for category in selection]
        if len(formatted_category) == 0:
            abort(404)

        return jsonify(
            {
                "success": True,
                "categories": formatted_category,
                "total_category": len(Category.query.all())
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
        #Get page number
        page = request.args.get("page", 1, type=int)       
        print(f'page_num:{page}' )
        CURRENT_CATEGORY_ID = page
        all_categories = Category.query.all()
        formatted_cat = {cat.id:cat.type for cat in all_categories}
             
        #print(f'selection:{selection}')
        current_category = formatted_cat[CURRENT_CATEGORY_ID]
        print(f"current_category:{current_category}")
        
        #print(f'current_question:{current_question}')        
        
        selection = Question.query.filter(Question.category ==CURRENT_CATEGORY_ID).order_by(Question.id).all() 
        #current_question = paginate_questions(request, selection)
        print(f'selection:{selection}')
        questions =  paginate_questions(request, selection)
        #questions = [question.format() for question in selection]
        print(f'questions:{questions}')
        #if len(questions) == 0:
            #abort(404)

        return jsonify(
            {
                "success": True,
                "questions": questions,
                "totalQuestion": len(selection),
                "currentCategory":current_category,
                "categories":formatted_cat,
            },
            
        )
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_book(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()
            selection = Question.query.order_by(Question.id).all()
            current_question = paginate_questions(request, selection)

            return jsonify(
                {
                    "success": True,
                    "deleted": question_id,
                    "books": current_question,
                    "total_books": len(Question.query.all()),
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
    @app.route("/question", methods=["POST"])
    def create_question():
        body = request.get_json()
        print(f'body:{body}')
        new_question = body.get("question", None)
        new_answer = body.get("answer", None)
        new_category = body.get("category", None)
        new_difficulty= body.get("difficulty",None)

        search= body.get("search",None)


        try:
            # if search:
            #     selection=Question.query.order_by(Question.id).filter(Question.question.ilike("%{}%".format(search)))
            #     current_questions=paginate_questions(request,selection)

            #     return jsonify(
            #         {
            #             "success": True,
            #             "questions": current_questions,
            #             "total_questions": len(selection.all()),
            #         })
            # else:
                question = Question(question=new_question, answer=new_answer, category=new_category,difficulty=new_difficulty)
                print(f'question:{question}')
                question.insert()

                selection = question.query.order_by(Question.id).all()
                current_questions = paginate_questions(request, selection)

                return jsonify(
                    {
                        "success": True,
                        "created": question.id,
                        "question": current_questions,
                        "total_books": len(Question.query.all()),
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

    @app.route("/question", methods=["POST"])
    def search_question():
        body = request.get_json()
        print(f'body:{body}')
        new_question = body.get("question", None)
        new_answer = body.get("answer", None)
        new_category = body.get("category", None)
        new_difficulty= body.get("difficulty",None)

        search= body.get("search",None)


        try:
            if search:
                selection=Question.query.order_by(Question.id).filter(Question.question.ilike("%{}%".format(search)))
                current_questions=paginate_questions(request,selection)

                return jsonify(
                    {
                        "success": True,
                        "questions": current_questions,
                        "total_questions": len(selection.all()),
                    })
            else:
                abort(404)
                # question = Question(question=new_question, answer=new_answer, category=new_category,difficulty=new_difficulty)
                # print(f'question:{question}')
                # question.insert()

                # selection = question.query.order_by(Question.id).all()
                # current_questions = paginate_questions(request, selection)

                # return jsonify(
                #     {
                #         "success": True,
                #         "created": question.id,
                #         "question": current_questions,
                #         "total_books": len(Question.query.all()),
                #     }
                # )

        except:
            abort(422)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

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

    @app.errorhandler(405)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 405, "message": "method not allowed"}),
            405,
        )

    return app

