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
    # TODO: Set up CORS. Allow '*'
    # '''
    CORS(app, resources={'/': {'origins': '*'}})

    # '''
    # TODO: Use  after request decorator to set Access-Control-Allow
    # '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response


#----------------------------------------------------------------------------#
# categories Routes.
#----------------------------------------------------------------------------#
# '''
# * GET requests for all available categories.
# '''
    @app.route('/categories', methods=['GET'])
    def all_categories():
        result = {}
        categories = Category.query.all()

        for category in categories:
            result[category.id] = category.type

        return jsonify({
            'categories': result
        })

    # '''
    # @TODO:
    #! Create an endpoint to handle GET requests for questions,
    # including pagination (every 10 questions).
    # This endpoint should return a list of questions,
    # number of total questions, current category, categories.
    # '''

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
        question = Question.query.get(id)
        question.delete()

        #  TODO I did test this by curl -i -X DELETE http://127.0.0.1:5000/questions/24 
        #  it deleted but because no return it show error

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
       
        new_question = Question(question, answer, category, difficulty)
        new_question.insert()
        return jsonify({
            'question': new_question.format()
        })
        # TODO" I Test Entering Data by curl -i -X POST -H 'Content-Type: application/json' -d '{"question": "NO WAY!", "answer": "HHA", "category":2 , "difficulty":1 }' http://127.0.0.1:5000/questions
        

    #! TEST: When you submit a question on the "Add" tab,
    # the form will clear and the question will appear at the end of the last page
    # of the questions list in the "List" tab.
    # '''

    # '''
    # @TODO:
    #! Create a POST endpoint to get questions based on a search term.
    # It should return any questions for whom the search term
    # is a substring of the question.

    #! TEST: Search by any phrase. The questions list will update to include
    # only question that include that string within their question.
    # Try using the word "title" to start.
    # '''

    # '''
    # TODO:  Create a GET endpoint to get questions based on category.
    # '''

    #! TEST: In the "List" tab / main screen, clicking on one of the
    # categories in the left column will cause only questions of that
    # category to be shown.
    # '''

    # '''
    #! @TODO:
    # Create a POST endpoint to get questions to play the quiz.
    # This endpoint should take category and previous question parameters
    # and return a random questions within the given category,
    # if provided, and that is not one of the previous questions.

    #! TEST: In the "Play" tab, after a user selects "All" or a category,
    # one question at a time is displayed, the user is allowed to answer
    # and shown whether they were correct or not.
    # '''

    # '''
    #! @TODO:
    # Create error handlers for all expected errors
    # including 404 and 422.
    # '''

    return app