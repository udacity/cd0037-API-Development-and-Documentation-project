import json
import os
from tkinter import N
from unicodedata import category, name
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
        response.headers.add("Access-Control-Allow-Headers",
                             "Content-Type,Authorization,true")
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,POST,OPTIONS,DELETE')

        return response
    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """


    @app.route('/categories', methods=['GET'])
    def get_all_questions():
        try:
            categories = Category.query.order_by(Category.id).all()

            formatted_Categories = {
                category.id: category.type for category in categories}
            return jsonify({
                "success": True,
                "categories": formatted_Categories,
                "total_categories": len(categories),

            })
        except:
            abort(404)

    """

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions', methods=['GET'])
    def get_paginated_questions():
        try:
            #get all questions but in a paginated format
            page = request.args.get('page', 1, type=int)
            start = (page - 1) * QUESTIONS_PER_PAGE
            end = start + QUESTIONS_PER_PAGE
            questions = Question.query.order_by(Question.id).all()
            formatted_questions = [question.format() for question in questions]
            categories = Category.query.order_by(Category.id).all()
            formatted_categories = {
                category.id: category.type for category in categories}
            return jsonify({
                "success": True,
                "questions": formatted_questions[start:end],
                "total_questions": len(Question.query.all()),
                "categories": formatted_categories
            })
        except:
            abort(404)

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):

        q_id = str(question_id)
        question = Question.query.filter(
            Question.id == q_id).one_or_none()
        if question is None:
            abort(404)
        question.delete()
        return jsonify({
            "success": True,
            "delete_id": question.id,
            "total_questions": len(Question.query.all())
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
    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()
        add_question = body.get('question', None)
        new_answer = body.get('answer', None)
        question_category = body.get('category', None)
        new_difficulty_score = body.get('difficulty', None)
        search_term = body.get('searchTerm', None)
        try:
            #check if there's a search_term in body
            if search_term:
                page = request.args.get('page', 1, type=int)
                start = (page - 1) * QUESTIONS_PER_PAGE
                end = start + QUESTIONS_PER_PAGE
                search_query = Question.query.filter(
                    Question.question.ilike(f'%{search_term}%')).all()
                formatted_search = [question.format()
                                    for question in search_query]
                return jsonify({
                    "success": True,
                    "questions": formatted_search[start:end],
                    "total_results": len(search_query)
                })
            else:
                new_question = Question(
                    question=add_question,
                    answer=new_answer,
                    category=question_category,
                    difficulty=new_difficulty_score
                )
            new_question.insert()
            return jsonify({
                "success": True,
                "created": new_question.id,
                "total_questions": len(Question.query.all())

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

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_question_based_on_category(category_id):
        try:
            #convert category_id to a string to validate tests as its passed as a string
            category = str(category_id)
            questions = Question.query.filter(
                Question.category == category).all()

            return jsonify({
                "success": True,
                "questions": [question.format() for question in questions],
                "total_questions": len(questions)
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
    def get_quiz_questions():
        body = request.get_json()
        category = body.get('quiz_category',None)
        previous_question = body.get('previous_questions')
        category_id = category['id']
        try:
            #if no category specified use the ALL category
            if category_id == 0:
                questions = Question.query.all()
            else:
                
                questions=Question.query.filter(Question.category==category_id).all()

                #return random questions from start=0, end len-1 of questions
            def random_questions():
                    return questions[random.randint(0,len(questions)-1)]

                #generate random questions for the next question
            next_question=random_questions()

            not_previous=True
            #get qustions not in previous category
            while (not_previous):
                if next_question.id in previous_question:
                    next_question=random_questions()
                else:
                    not_previous=False
            return jsonify({
                "success":True,
                "question":next_question.format()
            })
                


        except:
            abort(400)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not Found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Not processable"
        }), 422

    @app.errorhandler(400)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    return app
