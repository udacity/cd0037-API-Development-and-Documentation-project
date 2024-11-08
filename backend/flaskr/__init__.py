from tkinter import CURRENT
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
        page = request.args.get("page", 1, type=int)
        print(f'page_num:{page}' )
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        questions = [question.format() for question in selection]
        current_questions = questions[start:end]

        return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    if test_config is None:
        setup_db(app)
    else:
        database_path = test_config.get('SQLALCHEMY_DATABASE_URI')
        setup_db(app, database_path=database_path)

    CORS(app)
    with app.app_context():
        db.create_all()

     # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response
    
    #GET Categories
    @app.route("/categories", methods=["GET"])
    def retrieve_categories():
        try:
            categories = Category.query.order_by(Category.id).all()
            print(f'selection:{categories}' )
           
            formatted_category = {category.id:category.type for category in categories}
            print(f'formatted_category:{formatted_category}' )
            if len(formatted_category) == 0:
                 abort(404)

            response={
                    "categories": formatted_category,
                }
            return jsonify(response)
        except:
            abort(404)

    #GET Questions
    @app.route("/questions", methods=["GET"])
    def retrieve_questions():
        #Get page number
        page = request.args.get("page", 1, type=int)       
        print(f'page_num:{page}' )
        CURRENT_CATEGORY_ID = page
        try:
            all_categories = Category.query.all()
            formatted_cat = {cat.id:cat.type for cat in all_categories}
                
            #print(f'selection:{selection}')
            current_category = formatted_cat[CURRENT_CATEGORY_ID]
            print(f"current_category:{current_category}")
            
            #print(f'current_question:{current_question}')        

            selection = Question.query.filter(Question.category ==CURRENT_CATEGORY_ID).order_by(Question.id).all() 
            #print(f'selection:{selection}')
            if len(selection)>= 10:
                questions =  paginate_questions(request, selection)
            else:
                print(f'length: {len(selection)}')
                questions = [question.format() for question in selection]
            print(f'questions:{questions}')
            if len(questions) == 0:
                abort(404)

            response = {
                    "questions": questions,
                    "total_questions": len(Question.query.all()),                    
                    "categories":formatted_cat,
                    "current_category":current_category
                }

            return jsonify(response)
        except:
            abort(422)

   #DELETE Questions based on Question Id
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_book(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()
            selection = Question.query.order_by(Question.id).all()
            current_question = paginate_questions(request, selection)

            response = {
                    "success": True,
                    "deleted": question_id,
                    "question": current_question
                }
            return jsonify(response)

        except:
            abort(422)

    #POST Add Question and Search Question
    @app.route("/questions", methods=["POST"])
    def create_question():
        body = request.get_json()
        print(f'body:{body}')
        new_question = body.get("question", None)
        new_answer = body.get("answer", None)
        new_category = body.get("category", None)
        new_difficulty= body.get("difficulty",None)

        search= body.get("searchTerm",None)
        #print(f'search:{search}')

        try:
            if search:
                selection=Question.query.order_by(Question.id).filter(Question.question.ilike("%{}%".format(search))).all()
                #print(f'selection:{selection}')
                if len(selection)>=10:
                   current_question=paginate_questions(request,selection)
                else:
                   current_question = [question.format() for question in selection] 
                   #print(f'current_questions:{current_question}')

                response= {
                        "questions": current_question                       
                    }
                return jsonify(response)
            else:
                add_question = Question(question=new_question, answer=new_answer, category=new_category,difficulty=new_difficulty)
                print(f'question:{add_question}')
                add_question.insert()

                selection = add_question.query.filter(Question.category==new_category).order_by(Question.id).all()
                current_questions = paginate_questions(request, selection)

                response = {
                        "created": add_question.id,
                        "question": current_questions
                    }
                return jsonify(response)

        except:
            abort(422)

   #GET Questions based on Category Id  
    @app.route("/categories/<int:category_id>/questions", methods=["GET"])
    def retrieve_questions_by_category(category_id):
     try:
        all_categories = Category.query.all()
        formatted_cat = {cat.id:cat.type for cat in all_categories}
             
        #print(f'selection:{selection}')
        current_category = formatted_cat[category_id]
        #print(f"current_category:{current_category}")
        
        #print(f'current_question:{current_question}')        
        
        selection = Question.query.filter(Question.category ==category_id).order_by(Question.id).all() 
        if len(selection) == 0:
            abort(404)

        print(f'selection:{selection}')
        questions =  paginate_questions(request, selection)
       
        #print(f'questions:{questions}')      

        response =  {
                "questions": questions,
                "total_questions": len(selection),
                "current_category":current_category                
            }
        return jsonify(response)
     except:
            abort(422)
   
    #GET Questions based on current Category and previous questions and randomize next question     
    @app.route("/quizzes", methods=["POST"])
    def play_quiz():
        try:
            quiz_request = request.get_json()
        
            #print(f'body:{quiz_request}')
            previous_questions = quiz_request["previous_questions"]
            current_category_id = quiz_request["quiz_category"]["id"]

            #print(f'previous_questions:{previous_questions}')
            #print(f'quiz_category:{current_category_id}')
       
            if (current_category_id ==0):
                questions_in_category = db.session.query(Question.id).all()
            else:
                questions_in_category = db.session.query(Question.id).filter(Question.category==current_category_id).all()
            
            flat_question_in_cat = [i for sub in questions_in_category for i in sub ]
            filtered_questions_in_category = [q for q in flat_question_in_cat if q not in previous_questions]

            if (len(filtered_questions_in_category)==0):
                response = {"question":None}
            else:
                new_question_id = random.choice(filtered_questions_in_category)
                question = db.session.get(Question,new_question_id)
                response = {"question":question.format()}
            return jsonify(response)
        except:
           abort(422)

    #Error Handling
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "bad request"}), 400

    @app.errorhandler(405)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 405, "message": "method not allowed"}),
            405,
        )

    return app

