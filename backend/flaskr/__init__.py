from flask import Flask, request, abort, jsonify
from flask_cors import CORS
import random
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    
    questions = [question.format() for question in selection]
    current_questions = questions[start:end]
    
    return current_questions

def create_app(test_config=None):
    # creating and configuring the app
    app = Flask(__name__)
    setup_db(app)

    # Setting up CORS
    CORS(app, resources={r'/*': {'origins':'*'}})
    # CORS(app)
    
    # Using the after_request decorator to set Access-Control-Allow
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response
    
    # Retrieves all available categories
    @app.route("/categories", methods=["GET"])
    def get_categories():
        all_categories = Category.query.order_by(Category.id).all()
        
        if len(all_categories) == 0:
            abort(404)
            
        return jsonify(
            {
                "success": True,
                "categories": [category.format() for category in all_categories]
            }
        )

    # Retrieves all available questions
    @app.route("/questions", methods=["GET"])
    def get_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)
        
        if len(current_questions) == 0:
            abort(404)
            
        all_categories = [category.format() for category in Category.query.order_by(Category.id).all()]
        
        data_categories = {}
        for category in all_categories:
            data_categories[category['id']] = category['type']
            
        return jsonify(
            {
                "success": True,
                "questions": current_questions,
                "total_questions": len(selection),
                "current_category": "All",
                "categories": data_categories
            }
        )
    
    # Delete question using a giving id
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()
            
            if question is None:
                abort(404)
                
            question.delete()
            
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)
            
            return jsonify(
                {
                    "success": True,
                    "deleted": question_id,
                    "questions": current_questions,
                    "total_questions": len(selection)
                }
            )
        except:
            abort(422)
    
    # Create a new question, search a question by giving search_term if provide
    @app.route("/questions", methods=["POST"])
    def create_question():
        try:
            body = request.get_json()
            
            new_question = body.get("question", None)
            new_answer = body.get("answer", None)
            new_difficulty = body.get("difficulty", None)
            new_category = body.get("category", None)
            search_term = body.get("searchTerm", None)
            
            if "searchTerm" in body:
                if search_term == "":
                    abort(422)
                
                questions = Question.query.order_by(Question.id).filter(Question.question.ilike("%" + search_term + "%")).all()
                
                returned_questions = [question.format() for question in questions]
                
                return jsonify(
                    {
                        "success": True,
                        "questions": returned_questions,
                        "current_category": "All",
                        "total_questions": len(returned_questions)
                    }
                )
                
            else:
                if new_question == "" or new_answer == "":
                    abort(422)
                    
                question = Question(question=new_question, answer=new_answer, difficulty=new_difficulty, category=new_category)
                question.insert()
                
                selection = Question.query.order_by(Question.id).all()
                current_questions = paginate_questions(request, selection)
                
                return jsonify(
                    {
                        "success": True,
                        "created": question.id,
                        "questions": current_questions,
                        "total_questions": len(selection)
                    }
                )
        except:
            abort(422)
    
    # Creating a GET endpoint to get questions based on category.
    @app.route("/categories/<int:category_id>/questions", methods=["GET"])
    def get_questions_by_category(category_id):
        selection = Question.query.order_by(Question.id).filter_by(category = category_id).all()
        current_questions = paginate_questions(request, selection)
        category = Category.query.filter_by(id = category_id).one_or_none()
        
        if len(current_questions) == 0 or category.id is None:
            abort(404)
            
        return jsonify(
            {
                "success": True,
                "questions": current_questions,
                "current_category": category.type,
                "total_questions": len(selection)
            }
        )
    
    # Creating a POST endpoint to get questions to play the quiz.
    @app.route("/quizzes", methods=["POST"])
    def playing_game():
        try:
            body = request.get_json()
            previous_questions = body.get('previous_questions')
            quiz_category = body.get('quiz_category')
            
            if 'previous_questions' not in body and 'quiz_category' not in body:
                abort(422)
            
            if  quiz_category['id'] != 0 and quiz_category['type'] != "click":
                category = Category.query.get(quiz_category['id'])
                
                if category is None:
                    abort(422)
                    
                all_questions = Question.query.filter_by(category=quiz_category['id']).filter(Question.id.not_in(previous_questions)).all()
                questions_formatted = [question.format() for question in all_questions]
                
                # generate random question
                if len(questions_formatted) != 0:
                    question = random.choice(questions_formatted)
                    
                return jsonify({
                    "success": True,
                    "question": question
                })                
            else:
                all_questions = Question.query.filter(Question.id.not_in(previous_questions)).all()
                questions_formatted = [question.format() for question in all_questions]
                
                # generate random question
                if len(questions_formatted) != 0:
                    question = random.choice(questions_formatted)
                
                return jsonify({
                    "success": True,
                    "question": question
                })
        except:
            abort(422)

    # Creating error handlers for all expected errors
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify(
            {
                "success": False,
                "error": 400,
                "message": "bad request"
            }
        ), 400
        
    @app.errorhandler(404)
    def not_found(error):
        return jsonify(
            {
                "success": False,
                "error": 404,
                "message": "resource not found"
            }
        ), 404
        
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify(
            {
                "success": False,
                "error": 405,
                "message": "method not allowed"
            }
        ), 405
        
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify(
            {
                "success": False,
                "error": 422,
                "message": "unprocessable"
            }
        ), 422
        
    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify(
            {
                "success": False,
                "error": 500,
                "message": "internal server error"
            }
        ), 500

    return app

