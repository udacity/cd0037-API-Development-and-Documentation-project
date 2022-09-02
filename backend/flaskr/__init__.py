import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
        page = request.args.get('page',1,type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        questions = [question.format() for question in selection]
        currentQuestions = questions[start:end]
        return currentQuestions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    
    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app,resources={r"/*":{'origins':'*'}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories' ,methods=['GET'])
    def get_categories():
      try:  
        select_cat = Category.query.order_by(Category.id).all()
        categories = { category.format()['id'] :category.format()['type']  for category in select_cat}
        return jsonify({
            'success': True,
            'categories':categories
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
    def get_questions():
      try:  
        select_qts = Question.query.order_by(Question.id).all()
        current_qts = paginate_questions(request,select_qts)
        
        categories = Category.query.all()
        format_cat ={ category.format()["id"]: category.format()["type"]  for category in categories }

        if len(current_qts)==0 or len(format_cat) == 0 :
            abort(404)
        return jsonify({
            'success': True,
            'questions':current_qts,
            'totalQuestions':len(current_qts),
            'categories':format_cat,
            'currentCategory': None
        }), 200    
      except:
           abort(422)

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:qts_id>' ,methods=['DELETE'])
    def delete_question(qts_id):
        try:
            question = Question.query.filter( Question.id == qts_id).one_or_none()
            if question is None:
                abort(404)
            question.delete()    
            return jsonify({
                "success": True,
                "message": f"Question with id:{qts_id} is deleted"
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
    @app.route('/questions', methods=['POST'])
    def create_question():
        try:
            question = Question(question=request.get_json()['question'],answer=request.get_json()['answer'],category=request.get_json()['category'],difficulty=request.get_json()['difficulty'])
            question.insert()

            select_qts = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, select_qts) 
            
            return jsonify({
                "success": True,
                "message":"Question ceated successfully"
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
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        request_data = request.get_json()
        if 'searchTerm' not in request_data:
            abort(400) 
        search_term = request_data['searchTerm']
        questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
        return jsonify({
                "success":True,
                "questions":[question.format() for question in questions],
                "totalQuestions":len(questions),
                "currentCategory": None
            }) 
    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:cat_id>/questions', methods=['GET'])
    def get_question_by_category(cat_id):
        category = Category.query.filter_by(id = cat_id).one_or_none()
        try:
            questions = Question.query.filter_by(category = category.id ).all()
            question_list = paginate_questions(request, questions) 
            return jsonify({
                "success":True,
                "questions":question_list,
                "totalQuestions":len(question_list),
                "currentCategory":category.type
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
    @app.route('/quizzes',methods=['POST'])
    def get_quiz_questions():
        try:
            body = request.get_json()
            previous_questions = body.get('previous_questions')
            questions = Question.query.all()
            quiz_category = body.get('quiz.category')

            if(len(previous_questions) == len(questions)):
                return jsonify({
                    'success': True,
                    'message': 'game over'
                }), 200
            if quiz_category:
                result = Question.query.filter_by(category=quiz_category['id']).filter(Question.id.notin_(previous_questions)).all()
            else:
                result = Question.query.filter(Question.id.notin_(previous_questions)).all()        
            next_question = random.choice(result)
            while next_question.id in previous_questions:
                return jsonify({
                    'success': True,
                    'message':'game over'
                }), 200    
            while next_question.id not in previous_questions:
                return jsonify({
                    'success':True,
                    'question': next_question.format()
                })
        except:
            abort(400)  
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
            "message":"Not found"
        }), 404
    
    @app.errorhandler(422)
    def unprocessable(error):
      return jsonify({
        "success": False, 
        "error": 422,
        "message": "Unprocessable"
      }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request"
        }), 400

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal server error"
        }), 500
    return app

