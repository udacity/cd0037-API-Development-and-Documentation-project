import json
import os
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
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers","Content-Type,Authorization,true")
        response.headers.add('Access-Control-Allow-Methods','GET,POST,OPTIONS,DELETE')

        return response
    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories',methods=['GET'])
    def get_all_questions():
        try:
            categories=Category.query.order_by(Category.id).all()
            formatted_categories=[category.format() for category in categories]
            return jsonify({
                "success":True,
                "categories":formatted_categories,
                "total_categories":len(categories)
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
    @app.route('/questions',methods=['GET'])
    def get_paginated_questions():
        try:
            page=request.args.get('page',1,type=int)
            start=(page -1) * QUESTIONS_PER_PAGE
            end=start + QUESTIONS_PER_PAGE
            questions=Question.query.order_by(Question.id).all()
            current_category=[question.format() for question in questions]
            return jsonify({
                "success":True,
                "books":current_category[start:end],
                "total_questions":len(Question.query.all())
            })
        except:
            abort(404)
    
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>',methods=['DELETE'])
    def delete_question(question_id):
        question=Question.query.filter(Question.id==question_id).one_or_none()
        if question is None:
            abort(422)
        question.delete()
        return jsonify({
            "success":True,
            "delete_id":question.id,
            "total_questions":len(Question.query.all())
        })
    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.
    
    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions',methods=['POST'])
    def create_question():
        body=request.get_json()
        add_question=body.get('question',None)
        new_answer=body.get('answer',None)
        question_category=body.get('answer',None)
        new_difficulty_score=body.get('difficulty',None)
        try:
            new_question=Question(
                question=add_question,
                answer=new_answer,
                category=question_category,
                difficulty=new_difficulty_score
            )
            new_question.insert()
            return jsonify({
                "success":True,
                "created":new_question.id,
                "total_questions":len(Question.query.all())

            })
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
    @app.route('/questions/search',methods=['POST'])
    def search_question():
        body=request.get_json()
        search_term=body.get('searchTerm',None)
        try:
            if search_term:
                page=request.args.get('page',1,type=int)
                start=(page -1)* QUESTIONS_PER_PAGE
                end=start +QUESTIONS_PER_PAGE
                search_query=Question.query.filter_by(Question.question.ilike('%'+search_term+'%')).all()
                formatted_search=[question.format() for question in search_query]
                return jsonify({
                    "success":True,
                    "questions":formatted_search[start:end],
                    "total_results":len(search_query)
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
    @app.route('/categories/<int:category_id>/questions',methods=['GET'])
    def get_question_based_on_category(category_id):
        questions=Question.query.filter(Question.category==category_id).all()

        return jsonify({
            "success":True,
            "questions":[question.format() for question in questions],
            "total_questions":len(questions)
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

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    return app

