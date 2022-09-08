import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from collections.abc import Mapping
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10
#hdado
def paginate_questions(request, q_selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) *  QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in q_selection]
    current_questions = questions[start:end]

    return current_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app) 
    #i have updated !flask-cors to bypass an error 

    """
    testing: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    """
    @done: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response
    """
    @on_going:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    #get request for all categories : 
    #let's comunicate with the categories list in the databse and retreive it to the front-end: ---
    @app.route('/categories') #default method get 
    def retreive_categories():
        selection_categories = Category.query.order_by(Category.id).all()
        
        if len(selection_categories): #if the selection exist , lenght > 0, print json below  
            return jsonify(
                {
                "success" : True,
                "categories" : {c.id : c.type   for c in selection_categories},
                "total_category" : len(Category.query.all()) 
                }
        ) 
        else : #afficher erreur 404! not found error
            abort(404)

    """
    @on_going!!:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions,  current category ,* categories. <---- important

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    #pagination ! 10 item per page  , declared in top page
    #get request for questions : 
    # using : curl  http://127.0.0.1:5000/questions  is working fine
    @app.route("/questions", methods=["GET"])
    def retrieve_question():
        q_selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, q_selection)
        select_all_cat = Category.query.order_by(Category.id).all()
        formatted_categories = {c.id : c.type  for c in select_all_cat} #key value dict to represent formatted categories
        

        if len(q_selection)==0:
            abort(404)
        return jsonify(
            {
                "success" : True,
                "questions" : current_questions,  #Reminder to test later  
                "total_questions" : len(q_selection) ,#num of total question
                "categories": formatted_categories #show availlable categories
                 
            }
        )    


    """
    @done:
    Create an endpoint to DELETE question using a question ID.
    
    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    #building the delete endpoint for questionID
    @app.route("/questions/<int:question_id>", methods =['DELETE'])
    def delete_question(question_id):
        try:
            #query the database to extract question with the same id and match it with our endpoint question_id
            question = Question.query.filter(Question.id==question_id).one_or_none()
            if question is None: #flag an error 404 immediatly if the db query is none
                abort(404)

            question.delete()
            q_selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, q_selection)   

            return jsonify(
                {
                    "success" : True,
                    "deleted" : question_id,
                    "questions" : current_questions,
                    "total_questions" : len(Question.query.all()),
                }
            ) 
        except:
            abort(422)




    """
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    #let's begin, first post endpoint, so ; main objectif to post a new question
    #proceeding just like the bookshelf excercice in our course :
    @app.route("/questions", methods=["POST"])
    #i could have added GET and POST in the same app.route with if statment. 
    def create_question():
        body = request.get_json()

        new_question = body.get('question',None) #if any of the entries is empty, set it to NONE
        new_answer = body.get('answer', None)
        new_category = body.get('category', None)
        new_difficulty = body.get('difficulty', None)

        try:
            question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
            question.insert() #insert to database

            q_selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, q_selection)

            return jsonify(
                {
                    "success" : True,
                    "created" : question.id,
                    "questions" : current_questions,
                    "total_questions": len(Question.query.all()),
                }   
            )
        
        except:
            abort(422)
    #i have added questions succesfuly with curl -X POST -H "Content-type:application/json" -d'{}' http//:127.0.0.1:5000/questions
    # {} ----> {"question":"xxxxx", "answer": " xxxx", "category":"3".....} , i got question from trivia generator website. 
    """
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions/search', methods=["POST"])
    def search_question():
        #now api would get the keyword or text enter in front-end and compare it with our questions in db 
        body = request.get_json()
        search_term = body.get('searchTerm', None)

        #Now we have the searchTerm from the front-end (QuestionView), let's query the db and compare the searchTerm with any string question
        try:
            q_match = Question.question.ilike(f'%{search_term}%') #questions from table ilike==match searchTerm from request
            matched_search = Question.query.filter(q_match).all() #filter questions from db only by that are like the search term
            #flaf error 404 if query result is empty:
            if matched_search is None:
                abort(404)
            #we should not forget to add pagination and view the question as it should be done, because matched selection of question could > 10
            q_selection = matched_search #q_selection is now matched search
            current_questions = paginate_questions(request, q_selection) #pagination
            
            
            return jsonify(
                {
                    "success" : True,
                    "questions": current_questions, 
                    "total_questions": len(matched_search),
                
                }
            )
        except:
            abort(422)    

    """
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    #get questions based on category, that mean we have category page, then we open question from it
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def questions_from_category(category_id):
        #let's get category from db 
        #query_category = Category.query.filter_by(id=category_id).one_or_none() drop this query method after not getting a logic to call it in selection
        try:
            if category_id > len(Category.query.all()):
                abort(404)
            else:    
            #testing order_by , didn't get correct result/ 
                q_selection = Question.query.order_by(Question.id).filter(Question.category==category_id)  
                if q_selection is None:
                    abort(404) #not found
            #adding filter  to clean the output from Questions query and leave only question category that match the input ID <category_id> 
        #pagination :
                current_questions = paginate_questions(request, q_selection)

                return jsonify(
                    {
                    "success": True,
                    "questions": current_questions,
                    "total_questions" : len(Question.query.all()),
                
                    }
                    )
        except:
            abort(422) 
    # testing and working with : curl  http://127.0.0.1:5000/categories/3/questions  or any other number,
    # should added error for category number that doesn't exist       

    """
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    #inspecting in google chrome ; payload show that quiz_category: {type: "Science", id: "1"} / 
    # type in all :quiz_category: {type: "click", id: 0} , so let's get use of this information in our endpoint build  
    @app.route('/quizzes', methods=['POST'])
    def play_quizzes():
        # get the qestion category an the previous question
        body = request.get_json()
        quizCategory = body.get('quiz_category')
        previousQuestion = body.get('previous_questions')
        #let's set a logic: previous question list is empty [] in the first time playing the quiz game,  

        #first let's chose a category of questions to be asked in the quiz game : 
        try:
            if (quizCategory['type'] == 'click'): # when user click All / type = click or id == 0 
                possible_questions = Question.query.all()
            else: #user choose any category in the list : getting question from category with same id  
                possible_questions = Question.query.filter_by(category=quizCategory['id']).all()
            
            #let's use the random library to generate a random question  
            #random.randint(start, stop) 
            randomIndex = random.randint(0, len(possible_questions)-1)
            quizQuestion = possible_questions[randomIndex] 

            asked = False 
            if quizQuestion.id in previousQuestion:
                asked = True
                
            while not asked:
                quizQuestion = possible_questions[randomIndex] #randomIndex represent one random ID from availlable question id's 
                return jsonify({ #data as expected in fontend-- see read me front-end
                    'success': True,
                    'question': {
                        "id": quizQuestion.id,
                        "question": quizQuestion.question,
                        "answer": quizQuestion.answer,
                        "difficulty" : quizQuestion.difficulty,
                        "category": quizQuestion.category,
                        
                    },
                    'previousQuestion': previousQuestion
                })
                


                
        except Exception as e:
            print(e)
            abort(404)
       

    """
    @Done:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request_error(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'method not allowed'
        }), 405
    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500   

    return app

