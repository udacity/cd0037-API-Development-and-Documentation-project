#from crypt import methods
import os
import sys
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app)
    #cors = CORS(app,resources={r"/api/*":{"origins":"*"}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers","Content-Type, Authorization,True")
        response.headers.add("Access-Control-Allow-Methods","GET,PUT,POST,DELETE,OPTIONS")
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories', methods=['GET'])
    def get_categories():
        try:
            categories = Category.query.order_by(Category.id).all()
            #categories = category_format()
            #formatted_category =[c.format() for c in categories]
            return jsonify({
                'Success':True,
                'categories':{category.id: category.type for category in categories},
                })    
        except Exception:
            abort(422)


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
    # pagination method
    def paginate_question(request,selection):
        page = request.args.get('page',1, type=int)
        start = (page-1)*QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        formatted_questions =[question.format() for question in selection]
        format_questions = formatted_questions[start:end]
        return format_questions
      # end point for retrieving all the questions
    @app.route('/questions', methods=['GET'])
    def get_questions():
        try:
            # get all questions.
            questions = Question.query.order_by(Question.id).all()
            # paginate the questions retrieved from the db
            formatted_questions = paginate_question(request,questions)
            # get all categories
            categories= Category.query.order_by(Category.id).all()
            formatted_category = {category.id:category.type for category in categories}
            # check if there's no questions
            if len(formatted_questions) == 0:
                abort(404)
            else:
                return jsonify({
                    'success': True,
                    'questions':formatted_questions,
                    'total_questions': len(questions),
                    'categories': formatted_category,
                    'current_category':None,
                })
        except Exception as er:
            if '404' in str(er):
                abort(404)
            else:
                abort(422)    
    # testing the retrieve questions endpoint

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    # delete question endpoint
    @app.route('/questions/<int:question_id>',methods=['DELETE'])
    def delete_question(question_id):
        try:
            q = Question.query.filter_by(Question.id == question_id).one_or_none()
            # check if question exists
            if q is None:
                abort(404)
            q.delete()
            current_questions = paginate_question(request,q)
            return jsonify({
                'success':True,
                'deleted':question_id,
                'questions':current_questions,
                'number_of_questions':len(Question.query.all()),
            })
        except Exception as er:
            if '404' in str(er):
                abort(404)
            else:
                abort(422)    
    # test the delete question endpoint

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    # create a question endpoint
    @app.route('/create_question', methods=['POST'])
    def create_question():
        body = request.get_json()
        # question form fields
        new_question = body.get("question",None)
        new_answer = body.get("answer", None)
        new_difficulty = body.get("difficulty",None)
        new_category = body.get("category",None)
        
        try:
            question = Question(question=new_question,answer=new_answer,difficulty=new_difficulty,category=new_category)
            #insert the new question into the db
            question.insert()
            # display the new question on the list
            q = Question.query.order_by(Question.id).all()
            all_questions = paginate_question(request,q)
            # display in json
            return jsonify({
                'success':True,
                'created': question.id,
                'questions':all_questions,
                'total_questions':len(Question.query.all())
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
    @app.route('/search',methods=['POST'])
    def search_question():
        body = request.get_json()
        search = body.get('searchTerm',None)
        try:
            # query the questions table for the search term
            searchz = Question.query.order_by(Question.id).filter(Question.question.ilike("%{}%".format(search)))
            # add the search result on to the question list
            search_ques = paginate_question(request,searchz)
            # return the response in json format
            return jsonify({
                'success':True,
                'questions': search_ques,
                'total_questions': len(searchz.all()),
            })
        except Exception:
            abort(422)


    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:id>/questions')
    def get_questions_by_category(id):
        try:
            # get the category based on the category id
            categ = Category.query.filter(Category.id == id).one_or_none()
            # check if the category exists
            if categ is None:
                abort(404)
            else:
                # get questions based on the category
                selection = Question.query.filter(Question.category == id).limit(QUESTIONS_PER_PAGE).all()
                # make sure that all questions are paginated.
                questionz = paginate_question(request,selection)
                # return the response in json format.
                return jsonify({
                'success':True,
                'questions':questionz,
                'total_questions':len(selection),
                'current_category':Category.query.get(id).format(),
                })
        except Exception as er:
            if '404' in str(er):
                abort(404)
            else:
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
    def ids_from_questions(questions,previous_id):
        #create a formatted list of the current questions and compare both list and return to the list
        quuestions_formatted = [q.format() for q in questions]
        current_ids =[q.get('id') for q in quuestions_formatted]
        ids = list(set(current_ids).difference(previous_id))
        return ids

    @app.route('/quizzes',methods=['POST'])
    def get_questions_for_quiz():
        try:
            # get all the request from the body
            questionz = None
            body = request.get_json()
            category_quiz = body.get('quiz_category',None)
            past_ids = body.get('previous_questions',None)
            category_id = category_quiz.get('id')
            # check category
            if category_id == 0:
                # get all questions
                questionz = Question.query.all()
            else:
                #get questions by the requested category
                questionz = Question.query.filter(Question.category == category_id).all()
            print(questionz)
            # get the id list
            ids = ids_from_questions(questionz,past_ids)
            # check if the list is empty retirn no question
            if len(ids) == 0:
                return jsonify({
                    'success':True,
                    'question':None
                })
            else:
                random_id = random.choice(ids)
                # get the question
                question = Question.query.get(random_id)
                return jsonify({
                    'success':True,
                    'question':question.format()
                })
        except: 
            print(sys.exc_info())
            abort(422)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    # 422 Error Handler
    @app.errorhandler(422)
    def unprocessable(error):
        return (jsonify({
            'success':False,
            'error':422,
            'message': 'unprocessable',
        }),422
        )
    # 404 Error Handler
    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            'success':False,
            'error':404,
            'message': 'Resource Not Found'
        }),404
    # 500 error handler
    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success':False,
            'error': 500,
            'message':'Internal Server Error'
        }),500

    return app

