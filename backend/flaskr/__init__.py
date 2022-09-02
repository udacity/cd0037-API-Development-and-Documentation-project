import os
from select import select
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category


# Categories Function
def get_categories_func():
    categories = Category.query.order_by(Category.id).all()
    category_obj={}
    for category in categories:
        category_obj[category.id] = category.type
    return category_obj


# Pagination
QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start =  (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    books = [question.format() for question in selection]
    current_questions = books[start:end]

    return current_questions

def create_app(test_config=None):

    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

#   Initialize Cors
    CORS(app, resources={r"*": {"origins": "*"}})

#   After Request
    @app.after_request
    def after_request(response):
      response.headers.add("Access-Control-Allow-Headers","Content-Type,Authorization,true")  
      response.headers.add("Access-Control-Allow-Methods", "POST,GET,PUT,DELETE,OPTIONS")
      return response
   
    
# GET Categories
    @app.route('/categories', methods = ['GET'])
    def get_categories():
        categories = get_categories_func()

        return jsonify({
            'success':True,
            'categories': categories
        })

#  GET Questions
    @app.route('/questions', methods=['GET'])
    def get_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)
        categories = get_categories_func()
        if len(current_questions) == 0:
            abort(404)
        else:
            return jsonify({
                'success': True,
                'categories': categories, 
                'total_questions': len(Question.query.all()),
                'questions':current_questions,
            })


#    DELETE Question
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.get(question_id)

        if question is not None:
            question.delete()
            
            return jsonify({
                'success':True
            })
        else:
            abort(404)

#  Add And Search Questions
    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()
        new_question = body.get('question',None)
        new_answer = body.get('answer',None)
        new_difficult = body.get('difficulty',None)
        new_category = body.get('category', None)
        search = body.get('searchTerm',None)

        if search:
            selection = Question.query.order_by(Question.id).filter(Question.question.ilike('%{}%'.format(search)))
            current_question = paginate_questions(request, selection)
            return jsonify({
            'success': True,
            'questions':current_question,
            'totalQuestions':len(Question.query.all()),
            'currentCategory': 'Entertainment'
            })

        else:
            add_question = Question(
                question = new_question, 
                answer = new_answer,
                difficulty= new_difficult,
                category= new_category
            )

            add_question.insert()

            return jsonify({
                'success':True
            })
        
  
#    GET Questions Based on Categories
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_category(category_id):
        selection = Question.query.order_by(Question.id).filter(Question.category == category_id)
        current_questions = paginate_questions(request,selection)
        if selection:
            return jsonify({
                'questions':current_questions,
                'totalQuestions': len(Question.query.all()),
                'currentCategory': Category.query.get(category_id).type
            })
        else:
            abort(404) 
  
#   POST Random Quizz
    @app.route('/quizzes', methods=['POST'])
    def get_rand_quiz():
        body = request.get_json()
        print('Hello here')
        prev_questions = body.get('previous_questions',None) 
        quizz_cat = body.get('quiz_category',None)
       
        questions = Question.query.order_by(Question.id).filter(Question.category == quizz_cat['id'])
        selected_question = []
        for question in questions:
            if question.id not in prev_questions:
                selected_question.append(question)
        rand_idx = random.randrange(len(selected_question))
        random_question = selected_question[rand_idx]
        

        return jsonify({
            'success': True,
            'question': random_question.format()
        })
    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_foubd(error):
        return jsonify({
            'success': False,
            "error": 404,
            "message": "Not found"
        }), 404

    @app.errorhandler(405)
    def not_foubd(error):
        return jsonify({
            'success': False,
            "error": 405,
            "message": "Method Not Allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False, 
            "error": 422,
            "message": "unprocessable"
            }), 422

    return app

