import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import json

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginated_questions(model):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    
    formated_question = [question.format() for question in model)
    current_formated_questions = formated_question[start:end]
    
    return current_formated_questions
                         
                         

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers","Content-Type, Authorization, true")

        response.headers.add("Access-Control-Allow-Methods","GET, PATCH, POST, DELETE, OPTION")
        return response
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def categories():

        try:
            """ GET ALL CATEGORIES """
            all_categories = Category.query.order_by(Category.id).all()
            """ AND DICTIONARY OBJECT THE HOLDS ALL FORMATED CATEGORIES """        
            formated_categories = {}
                         
            for category in all_categories:
                formated_categories[category.id] = category.type

            return jsonify({
                "success": True,
                "categories": formated_categories,
            })
        except:
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
    def questions():

        all_questions = Question.query.order_by(Question.id).all()
        all_categories = Category.query.order_by(Category.id).all()
        current_questions = paginated_questions(all_questions)

        formated_categories = {}
        
        for category in all_categories:
            formated_categories[category.id] = category.type

        if len(current_questions) == 0:
            abort(404)
        else:
            return jsonify({
                "success": True,
                "questions": current_questions,
                "total_questions": len(all_questions),
                "categories": formated_categories,
                "current_category": "questions"
            })
                         
    
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):

        try:
            question = Question.query.get(question_id)
            question.delete()

            all_questions = Question.query.order_by(Question.id).all()
            current_questions = paginated_questions(all_questions)


            return({
                "success": True,
                "deleted_question": question.id,
                "questions": current_questions,
                "total_questions": len(current_questions)
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
    @app.route('/questions', methods=["POST"])
    def search_for_questions_or_create_a_question():

        body = request.get_json()

        question = body.get('question', None)
        answer = body.get('answer', None)
        category = body.get('category', None)
        difficulty = body.get('difficulty', None)
        search_term = body.get('searchTerm', None)
       

        try:
            if search_term:
                searched_questions = Question.query.filter(
                    Question.question.ilike(f'%{search_term}%'))
                current_questions = paginated_questions(searched_questions)

                return jsonify({
                    "success": True,
                    "questions": current_questions
                })
            else:
                new_question = Question(
                    question=question, answer=answer, category=category, difficulty=difficulty)

                new_question.insert()

                questions = Question.query.order_by(Question.id).all()
                current_questions = paginated_questions(questions)
                return jsonify({
                    "success": True,
                    "created": new_question.id,
                    "questions": current_questions,
                    "total_questions": len(questions)
                })
        except:
            abort(405)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions')
    def retrieve_questions_by_category(category_id):

        try:
            category = Category.query.get(category_id)
            all_questions = Question.query.filter(Question.category == category.id)
            formated_questions = [question.format() for question in all_questions]

            return({
                "success": True,
                "questions": format_questions,
                "totalQuestions": len(formated_questions),
                "current_category": category.type
            })

        except:
            abort(422)
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
                         
    @app.route('/quizzes', methods=["POST"])
    def get_quizzes():

        try:
            
            body = request.get_json()

            
            previous_questions = body.get('previous_questions')
            current_quiz_category = body.get('quiz_category')

            unanswered_questions = Question.query.filter(
                Question.category == current_quiz_category.get('id'))

            current_question = random.choice(
                [question for question in unanswered_questions if question.category not in previous_questions])

            random_question = {
                'id': current_question.id,
                'question': current_question.question,
                'answer': current_question.answer,
                'category': current_question.category,
                'difficulty': current_question.difficulty
            }

            return jsonify({
                'success': True,
                'question': random_question
            })
        except:
            abort(422)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource Not Found",
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable Entity"
        }), 422

    @app.errorhandler(405)
    def method_not_found(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method Not Allowed"
        }), 405

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400
                         
    
    return app

