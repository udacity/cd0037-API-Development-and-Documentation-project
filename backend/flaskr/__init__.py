import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from json import load
import time
time.clock = time.time

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10


def pag_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [quest.format() for quest in selection]
    current_questions = questions[start:end]
    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    
    ### @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs

    CORS(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    ### @TODO: Use the after_request decorator to set Access-Control-Allow
    
    @app.after_request 
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Origin", "*"
        )
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    ### @TODO: Create an endpoint to handle GET requests for all available categories.
    
    @app.route('/categories')
    def get_categories():
        # curl -X GET http://127.0.0.1:5000/categories

        catresult = db.session.query(Category).order_by(Category.id).all()

        if len(catresult) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'categories': {cat.id: cat.type for cat in catresult},
            'total_categories': len(catresult) 
        })

    # GET requests for questions including pagination (every 10 questions).
    # This endpoint returns a list of questions, number of total questions, current category, categories.
    @app.route('/questions')
    def get_req_questions():
        # curl -X GET http://127.0.0.1:5000/questions
        # curl -X GET http://127.0.0.1:5000/questions?page=2
        t_selection = Question.query.order_by(Question.id).all()
        t_curr_questions = pag_questions(request, t_selection)

        t_categories = Category.query.order_by(Category.type).all()

        if len(t_curr_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': t_curr_questions,
            'total_questions': len(t_selection),
            'categories': {cat.id: cat.type for cat in t_categories}
        })
    
    # DELETE question using a question ID.
    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_a_question(id):
        # curl -X DELETE http://127.0.0.1:5000/questions/<int:id>
        # curl -X DELETE http://127.0.0.1:5000/questions/25
        try:

            aquestion = Question.query.get(id)
            # del_question = Question.query(Question.question).filter(Question.id == id)

            if aquestion is None:
                abort(404)

            aquestion.delete()

            t_question = len(Question.query.all())

            return jsonify({
                'success': True,
                'deleted': id,
                # 'question_deleted': del_question,
                'total_questions': t_question
            })
        except:
            abort(422)
    
    # POST a new question, which will require the question and answer text, category, and difficulty score.
    @app.route('/questions', methods=['POST'])
    # curl -X POST http://127.0.0.1:5000/questions -H "Content-Type: application/json" -d '{"question": "test question", "answer": "test answer", "category": 5, "difficulty": "1" }'
    def add_new_question():
        # http://127.0.0.1:5000/questions
        bodyData = request.get_json()

        new_quest_result = bodyData.get('question')
        new_ans_result = bodyData.get('answer')
        new_cat_result = bodyData.get('category')
        new_diff_result = bodyData.get('difficulty')

        if (bodyData, new_quest_result, new_ans_result, new_cat_result, new_diff_result) == None:
            abort(422)

        try:
            newquestion = Question(
                question=new_quest_result,
                answer=new_ans_result,
                category=new_cat_result,
                difficulty=new_diff_result
            )

            newquestion.insert()

            t_questions = Question.query.all()
            curr_questions = pag_questions(request, t_questions)

            return jsonify({
                'success': True,
                'created': newquestion.id,
                'questions': curr_questions,
                'total_questions': len(t_questions)
            })
        except:
            abort(422)
    
    # POST endpoint to get questions based on a search term
    @app.route('/questions/search', methods=['POST'])
    # curl -X POST http://127.0.0.1:5000/questions/search -H "Content-Type: application/json" -d '{"searchTerm": "title"}'
    def searched_questions():
        body = request.get_json()
        searchTerm = body.get('searchTerm')
        
        # question = Question.query.all()

        if searchTerm == None:
            abort(404)
        if searchTerm:
            selected = Question.query.filter(
                Question.question.ilike(f'%{searchTerm}%')).all()
            searched_questions = pag_questions(request, selected)

            return jsonify({
                "success": True,
                "questions": searched_questions,
                "total_questions": len(selected)
            })
    
    # GET questions based on category.
    @app.route('/categories/<int:id>/questions', methods=['GET'])
    def categorized_questions(id):
        # curl -X GET http://127.0.0.1:5000/categories/2/questions
        
        category_query = Category.query.filter(Category.id == id).one_or_none()
        if category_query:

            filterquestion = Question.query.filter(
                    Question.category == id ).all()

            curr_questions = pag_questions(request, filterquestion)

        # if category_id > len(category_query):
        #     abort(404)

            return jsonify({
                "success": True,
                "questions": curr_questions,
                "total_questions": len(filterquestion),
                # "current_category": [my_str.join(cat.type) if cat.id == category_id else 'x' for cat in categories]
                "current_category": category_query.type
            })
        else:
            
            abort(404)
    
    # POST endpoint to get questions to play the quiz, 
    # This endpoint takes category and previous question parameters and returns a 
    # random question within the given category if provided, and that is not one of the previous questions.
    @app.route('/quizzes', methods=['POST'])
    def qplay_trivia():
        # curl -X POST http://127.0.0.1:5000/quizzes -H "Content-Type: application/json" -d '{"quiz_category": {"id": 2}, "previous_questions": []}'
        # curl -X POST http://127.0.0.1:5000/quizzes -H "Content-Type: application/json" -d '{"quiz_cat": {"id": 2}, "prev_questions": []}'
        try:
            bodyData = request.get_json()
            quiz_category = bodyData.get('quiz_category')
            previous_questions = bodyData.get('previous_questions')
            # cat_id = quiz_cat['id']
            # Question.id.notin_
            # previous_questions

            if quiz_category:
                questionlist = Question.query.filter(Question.category == quiz_category["id"]).all()

                if quiz_category["id"] == 0:
                    questionlist = Question.query.filter(Question.category == quiz_category["id"]).all()
            quizIds = [question.id for question in questionlist]
            # question = None
            # if(questionsresult):
            randomId = random.choice([random for random in quizIds if random not in previous_questions])

            question = Question.query(Question.id == randomId).one_or_none()

            return jsonify({
                'success': True,
                'question': question.format()
            })
        except:
            abort(422)
    
    ## Error Handler 400, 422. 404, 500 ##
    @app.errorhandler(404)
    def not_found(error):
        return(
            jsonify({
            'success': False, 
            'error': 404,
            'message': 'resource does not exists',
            'data': []
            }),
            404
        )

    @app.errorhandler(422)
    def unprocessed(error):
        return(
            jsonify({'success': False, 'error': 422,
                    'message': 'the request cannot be processed'}),
            422
        )

    @app.errorhandler(400)
    def bad_request(error):
        return(
            jsonify({'success': False, 'error': 400,
                    'message': 'Error. Invalid request'}),
            400
        )

    @app.errorhandler(405)
    def not_allowed(error):
        return(
            jsonify({'success': False, 'error': 405,
                    'message': 'Error. method not alllowed'}),
            405
        )

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            'error': 500,
            "message": "Internal server error"
        })

    return app
