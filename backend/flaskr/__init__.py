import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    formatted_questions = [question.format() for question in selection]
    current_questions = formatted_questions[start:end]

    return current_questions



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app) 

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    # @app.after_request
    # def after_request(response):
    #     response.headers.add('Acess-Control-Allow-Headers', 'Content-Type,Authorization,true')
    #     response.headers.add('Acess-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
    #     return response

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def retrieve_categories():
        try:
            category_obj ={}
            categories=Category.query.order_by(Category.id).all()
            formatted_categories = [category.format() for category in categories]
            for cat in formatted_categories:
                category_obj[str(cat['id'])] = cat['type']

            return jsonify({
                'success': True,
                'categories': category_obj
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
    @app.route('/questions/results')
    def retrieve_questions():
        category_obj ={}
        selection = Question.query.order_by(Question.id).all()
        categories = Category.query.order_by(Category.id).all()
        formatted_categories = [category.format() for category in categories]
        current_questions = paginate_questions(request, selection)
        for cat in formatted_categories:
            category_obj[str(cat['id'])] = cat['type']

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(Question.query.all()),
            'current_category': formatted_categories[current_questions[0]['category']-1]['type'],
            'categories': category_obj
        })

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:id>/deletes', methods=['DELETE', 'POST'])
    def delete_question(id):
        try:
            question = Question.query.filter(Question.id==id).one_or_none()

            if question is None:
                abort(404)

            question.delete()

            return jsonify({
                'success': True
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
        body = request.get_json()

        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_difficulty = body.get('difficulty', None)
        new_category = body.get('category', None)

        try:
            question =Question(question=new_question, answer=new_answer, difficulty=new_difficulty, category=new_category)
            question.insert()

            return jsonify({'success': True})
            
        except:
            abort(405)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions/searches', methods=['POST'])
    def search_questions():
        body = request.get_json()

        search_term = body.get('searchTerm', '')
        print('The search term is ', search_term)
        try:
            selection = Question.query.filter(Question.question.ilike('%{}%'.format(search_term))).all()
            current_search = paginate_questions(request, selection)
            categories = Category.query.order_by(Category.id).all()
            formatted_categories = [category.format() for category in categories]

            return jsonify({
                'success': True,
                'questions': current_search,
                'total_questions': len(selection),
                'current_category': formatted_categories[current_search[0]['category']-1]['type']
            })

        except:
            abort(404)




    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:id>/questions')
    def retrieve_categories_questions(id):
        questions = Question.query.filter(Question.category==id).order_by(Question.id).all()
        formatted_questions = [question.format() for question in questions]
        categories = Category.query.order_by(Category.id).all()
        formatted_categories = [category.format() for category in categories]
        current_category = formatted_categories[formatted_questions[0]['category']-1]['type']



        if len(formatted_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': formatted_questions,
            'total_questions': len(formatted_questions),
            'current_category': current_category
        })


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
    def quizzes_plays():
        body = request.get_json()

        quiz_category = body.get('quiz_category')
        quiz_category_id = quiz_category['id']
        previous_questions = body.get('previous_questions')

        try:
            if quiz_category_id != 0:
                questions = Question.query.filter(Question.category==quiz_category_id).all()
                formatted_questions = [question.format() for question in questions]
                possible_questions = []
                for quest in formatted_questions:
                    if quest['id'] not in previous_questions:
                        possible_questions.append(quest)
                question = possible_questions[random.randint(0, len(possible_questions)-1)]
                print(question)
            else:
                questions = Question.query.all()
                formatted_questions = [question.format() for question in questions]
                possible_questions = []
                for quest in formatted_questions:
                    if quest['id'] not in previous_questions:
                        possible_questions.append(quest)
                question = possible_questions[random.randint(0, len(possible_questions)-1)]

            return jsonify({
                'success': True,
                'question': question
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
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad_request'
        }), 400

    @app.errorhandler(405)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'method not allowed'
        }), 405

    return app

