import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_username = 'caryn'
        self.database_password = '1234'
        self.hostname = '127.0.0.1'
        self.port_number = '5432'
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}:{}/{}".format(
            self.database_username, self.database_password, self.hostname,
            self.port_number, self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """ Test Cases Related to categories Routes - 3 Test have Done"""

    def test_get_all_categories(self):
        response = self.client().get('/categories')
        data = json.loads(response.data)

        # make assertions on the response data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['categories']), 6)

    def test_get_filtered_questions_by_category(self):

        # Request data with category id 5
        response = self.client().get('/categories/5/questions')

        # loading the data
        data = json.loads(response.data)

        # check status code and message
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

        # check that questions is not empty
        self.assertNotEqual(len(data['questions']), 0)

    def test_category_id_not_found(self):

        # send request with category id 9999
        response = self.client().get('/categories/9999/questions')

        # load response data
        data = json.loads(response.data)

        # check response status code and message
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    """ Test Cases Related to questions Routes """
    def test_get_questions(self):
        response = self.client().get('/questions?page=1')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data['questions'], list)
        self.assertLessEqual(len(data['questions']), 10)
        self.assertIsInstance(data['total_questions'], int)

    def test_delete_question(self):
        question_id = 1
        response = self.client().delete(f'/questions/{question_id}')
        data = json.loads(response.data)
        if response.status_code == 404:
            self.assertEqual(data['success'], False)
        else:
            self.assertTrue(data['deleted'])

    def test_delete_question_fail(self):
        response = self.client().delete('/questions/0')
        data = json.loads(response.data)
        self.assertEqual(data['success'], False)


    def test_search_questions(self):

        # send post request with search term
        response = self.client().post(
            '/questions/search', json={'searchTerm': 'wh'})

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_search_questions_not_found(self):

        # send post request with search term
        response = self.client().post(
            '/questions/search', json={'searchTerm': ''})

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)

    """ Test Cases Related to quizzes Routes """
    def test_get_quiz_questions_found(self):
        data_json = {
            "previous_questions": [3, 4, 5, 10],
            "quiz_category": {"type": "Art", "id": 2}
                    }
       
        response = self.client().post('/quizzes', json=data_json)
        data = json.loads(response.data)
        # confirm the status response code is 200 is mean Ok
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['question'])

    def test_post_quiz_not_found(self):
        data = {
                "previous_questions": None,
                "quiz_category": None
                }
        response = self.client().post('/quizzes', json=data)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["success"], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
