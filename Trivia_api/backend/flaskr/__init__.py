import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from models import *


QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    # '''
    # * Set up CORS. Allow '*'
    # enable cross-domain requests and set response headers
    # '''
    CORS(app, resources={'/': {'origins': '*'}})

    # '''
    # * Use after request decorator to set Access-Control-Allow
    # '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response


#----------------------------------------------------------------------------#
# Routes.
#----------------------------------------------------------------------------#
# '''
# * GET requests for all available categories.
#
# '''
    @app.route('/categories', methods=['GET'])
    def all_categories():
        categories = Category.query.all()

        return jsonify({
            'categories': [Category.format()['type'] for Category in categories],
        })

    # '''
    # * GET requests for questions,
    # including pagination (every 10 questions).
    # This endpoint should return a list of questions,
    # number of total questions, current category, categories.
    # '''
    @app.route('/questions')
    def get_questions():
        Questions = Question.query.order_by(Question.id).all()
        Categories = Category.query.order_by(Category.type).all()
    
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        questions = [question.format() for question in Questions]
        current_questions = questions[start:end]

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(Questions),
            'categories': {category.id: category.type for category in Categories},
            'current_category': None
        })
    #  use http://127.0.0.1:5000/questions?page=(PageNumberHere)

    # '''
    #! TEST: At this point, when you start the application
    # you should see questions and categories generated,
    # ten questions per page and pagination at the bottom of the screen for three pages.
    # Clicking on the page numbers should update the questions.
    # '''

    # '''
    # * DELETE question using a question ID.
    # '''
    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):
        try:
            question = Question.query.get(id)
            question.delete()

            return jsonify({
                'success': True,
                'DELETED ID': id,
            })
            
        except:
            abort(422)

    #  tested this by curl -i -X DELETE http://127.0.0.1:5000/questions/25  & also by postman
   # '''
     #! TEST: When you click the trash icon next to a question, the question will be removed.
     # This removal will persist in the database and when you refresh the page.
    # '''


    # '''
    # * POST a new question, require the question and answer text, category, and difficulty score.
    # '''
    @app.route('/questions', methods=['POST'])
    def add_question():
        question = request.json.get('question')
        answer = request.json.get('answer')
        category = request.json.get('category')
        difficulty = request.json.get('difficulty')

        # Check if fields are empity or not
        if not (question and answer and category and difficulty):
            return abort(400)
                        
        new_question = Question(question, answer, category, difficulty)
        new_question.insert()
        return jsonify({
            'question': new_question.format()
        })
    # I Test Entering Data by curl -i -X POST -H 'Content-Type: application/json' -d '{"question": "NO WAY!", "answer": "HHA", "category":2 , "difficulty":1 }' http://127.0.0.1:5000/questions
    #! TEST: When you submit a question on the "Add" tab,
    # the form will clear and the question will appear at the end of the last page
    # of the questions list in the "List" tab.
    # '''


    # '''
    # * POST to get questions based on a search term.
    # return questions based on the search term
    # Substring of the question are allowed.
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        data = request.get_json()
        search_term = data.get('searchTerm', '')
        
        if search_term == '':
            abort(422)

        questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()

        # return response if successful
        return jsonify({
            'success': True,
            'questions': [question.format() for question in questions],
        }), 200

    #! TEST: Search by any phrase. The questions list will update to include
    # only question that include that string within their question.
    # Try using the word "title" to start.
    # '''


    # '''
    # * get questions filtered by (category type) category ID.
    # '''
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def questions_by_categoryID(category_id):
        try:
            query =  Question.query.filter(Question.category == category_id)
            questions = [question.format() for question in query]
                            
            return jsonify({
                'success': True,
                'questions': questions,
                'total_questions': len(questions),
            })

        except:
            abort(404)

    #! TEST: In the "List" tab / main screen, clicking on one of the
    # categories in the left column will cause only questions of that
    # category to be shown.
    # '''


    # '''
    # * Create a POST to get questions to play quiz.
    # This should take category and previous question parameters
    # and return a random questions within the given category,
    # and not one of the previous questions.
    @app.route('/quizzes', methods=['POST'])
    def quiz_question():
  
        data = request.get_json()
        previous_questions = data.get('previous_questions')
        quiz_category = data.get('quiz_category')

        # Check if quiz category and previous questions not empity
        if ((quiz_category is None) or (previous_questions is None)):
            abort(400)

        # Check if category is not specified which return all questions else specific category only
        if ( quiz_category == 0 ):
            questions = Question.query.all()
        else:
            questions = Question.query.filter_by( category = quiz_category ).all()
                
        # Function to generator random question  
        def get_random_question():
            return questions[random.randint(0, len(questions)-1)]

        # get next question
        next_question = get_random_question()

        # check if next question not on previous questions
        found = True

        # loop if found is true until found new question 
        while found:
            if next_question.id in previous_questions:
                next_question = get_random_question()
            else:
                found = False

        #retun the question
        return jsonify({
            'success': True,
            'question': next_question.format(),
        }), 200


    #! TEST: In the "Play" tab, after a user selects "All" or a category,
    # one question at a time is displayed, the user is allowed to answer
    # and shown whether they were correct or not.
    # '''



    # '''
    # * Check all Routes and Create error handlers for all expected errors
    # including 400, 404, 422 and 500 errors handlers. 
    # '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found. The requested page could not be found but may be available again in the future"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable, unable to process the contained instructions. Error realted to semantically erroneous"
        }), 422

    @app.errorhandler(400)
    def bad_syntax(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "The request cannot be fulfilled due to bad syntax"
        }), 400

    @app.errorhandler(500)
    def Server_Error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error."
        }), 500

    return app
