import os
from flask import (Flask, 
                request, 
                abort, 
                jsonify
            )
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1)* QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_question = questions[start:end]

    return current_question

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={r"/api/v1.0/*":{"origins":"*"}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization,true")
        response.headers.add("Access-Control-Allow-Methods", "GET,PATCH,POST,DELETE,OPTIONS")
        return response
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def list_categories():
        try:
            # Query all categories
            categories = Category.query.all()
            # return success and all categories in category.id:category.type
            return jsonify({
                "success": True,
                "categories": {category.id:category.type for category in categories}
            })

        except:
            # If any exception is encountered, abort
            abort(404)
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
    @app.route('/questions')
    def list_paginated_questions():
        try:
            # Query all questions in the db and order by id in ascending order
            selection = (
                Question.query
                .order_by(Question.id)
                .all()
            )
            # Paginate the questions queried above by passing it through the paginate function
            current_question = paginate_questions(request, selection)
            categories = Category.query.all()
            # Get the current category 
            current_category = (
                Category.query
                .filter(Category.id == selection[0].category)
                .one_or_none()
            )
            # If there are no questions returned, abort
            if len(current_question) == 0:
                abort(404)
            
            return jsonify({
                "success": True,
                "questions": current_question,
                "total_questions": len(Question.query.all()),
                "categories": {category.id:category.type for category in categories},
                "current_category": current_category.type
            })
        
        except:
            abort(404)
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        try:
            # Query the db by the question_id
            question = (
                Question.query
                .filter(Question.id == question_id)
                .one_or_none()
            )
            # If no questions are found, abort
            if len(question)== 0:
                abort(422)
            # Delete the filtered result
            question.delete()
        
            return jsonify({
                "success": True,
                "deleted": question_id,
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
    def add_question():
        # Retrieve new question attributes from the frontend
        body = request.get_json()
        new_question = body.get("question", None)
        new_answer = body.get("answer", None)
        new_difficulty = body.get("difficulty", None)
        new_category = body.get("category", None)
        search_term = body.get("searchTerm", None)
        
        if search_term:
            try:
                questions = (
                    Question.query
                    .filter(Question.question.ilike('%'+ search_term +'%'))
                    .order_by(Question.id)
                    .all()
                )
                #If no result, abort
                questions_found = len(questions)
            
                current_category = (
                    Category.query
                    .filter(Category.id == questions[0].category)
                    .one_or_none()
                )

                return jsonify({
                    "success": True,
                    "questions": [question.format() for question in questions],
                    "total_questions": len(questions),
                    "current_category": current_category.type
                })
            except:
                abort(404)
        else:
            try:
                # Create a new Question instance with the attributes received
                question = Question(
                    question = new_question,
                    answer = new_answer,
                    difficulty = new_difficulty,
                    category = new_category
                )
                # Insert into the db
                question.insert()
                selection = (
                    Question.query
                    .order_by(Question.id)
                    .all()
                )
                # Paginate the result
                current_question = paginate_questions(request, selection)
                categories = Category.query.all()
                current_category = (
                    Category.query
                    .filter(Category.id == selection[0].category)
                    .one_or_none()
                )
            
                return jsonify({
                    "success": True,
                    "created": question.id,
                    "questions": current_question,
                    "total_questions": len(Question.query.all()),
                    "categories": {category.id:category.type for category in categories},
                    "current_category": current_category.type
                })
        
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
            category = (
                Category.query
                .filter(Category.id == category_id)
                .one_or_none()
            )
            selection = (
                Question.query
                .filter(Question.category == category_id)
                .all()
            )
            current_question = paginate_questions(request, selection)
            
            if len(current_question) == 0:
                abort(404)

            return jsonify({
                "success": True,
                "questions": current_question,
                "total_questions": len(selection),
                "current_category": category.type
            })
        except:
            abort(404)
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
    @app.route('/quizzes', methods=['POST'])
    def get_quiz_question():
        #Retrieve and store quiz_category and previous_questions. Instantiate a question variable to hold question later
        quiz_category = request.json['quiz_category']
        previous_questions = request.json['previous_questions']
        question = None
        
        try:
            #If no quiz_category specified before, populate questions from db excluding previous_questions
            if (quiz_category['id'] == 0):
                questions = (
                    Question.query
                    .filter(Question.id.not_in(previous_questions))
                    .all()
                )
            #If quiz_category was specified, populate questions from the specified category excluding previous_questions
            else:
                questions = (
                    Question.query
                    .filter(Question.id.not_in(previous_questions), 
                    Question.category == quiz_category['id'])
                    .all()
                )
            #Find how many questions retrieved, and instantiate a counter to count the questions
            count_questions = len(questions)
            counter = 0
            #Create a while loop to retun questions provided counter is less than the questions
            while (counter < count_questions):
                question = random.choice(questions)
                
                return jsonify({
                    "success": True,
                    "question": question.format()
                })
                counter+=1
            #End the quiz when counter is equal to total questions retrieved from db in the given category
            if counter == count_questions:
                return jsonify({
                    "success": True,
                    "message": "game over"
                })
        except:
            abort(404)
    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({
                "success": False,
                "error": 404,
                "message": "resource not found",
            }), 
            404
        )
    
    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({
                "success": False,
                "error": 422,
                "message": "unprocessable entity",
            }), 
            422
        )

    @app.errorhandler(405)
    def method_not_allowed(error):
        return (
            jsonify({
                "success": False,
                "error": 405,
                "message": "method not allowed",
            }), 
            405
        )
    return app

