import unittest
import json
from models.dbmodels import DatabaseAccess
from app.api import app, api
from models.data import user1, user2, user3, user4, user5, user6, user7, question1, answer1

from run import api

BASE_URL = '/api/v1/'


class TestClass(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.cur = DatabaseAccess()
        self.cur.create_table_subscribers()
        self.cur.create_table_answer()
        self.cur.create_table_questions()

    # test user signup
    def test_user_added_successfully(self):
        response = self.app.post(
            '/api/v1/auth/signup', content_type="application/json", data=json.dumps(user1))
        self.assertEqual(response.json, {"msg": "success!"})
        self.assertEqual(response.status_code, 201)

    def test_user_attempts_missing_fields(self):
        response = self.app.post('{}auth/signup'.format(BASE_URL),
                                 content_type="application/json", data=json.dumps(user3))
        self.assertEqual(response.status_code, 400)
        self.assertNotIn("display_name", user3)

    def test_all_fields_are_filled(self):
        response = self.app.post('{}auth/signup'.format(BASE_URL),
                                 content_type="application/json", data=json.dumps(user4))
        self.assertEqual(response.status_code, 400)

    def test_user_invalid_email(self):
        response = self.app.post('{}auth/signup'.format(BASE_URL),
                                 content_type="application/json", data=json.dumps(user6))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {'error': 'Invalid email address'})

    def test_get_all_subscribers(self):
        response = self.app.get('{}auth/signup'.format(BASE_URL),
                                content_type="application/json", data=json.dumps(user6))
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json)

    # test user login

    def test_unregistered_user_login(self):
        login_response = self.app.post(
            '{}auth/login'.format(BASE_URL), content_type="application/json", data=json.dumps(user2))
        self.assertEqual(login_response.json, {
                         "error": "User bugingo doesn't exist"})
        self.assertEqual(login_response.status_code, 401)

    def test_user_logsin_successfully(self):

        login_response = self.app.post(
            '{}auth/login'.format(BASE_URL), content_type="application/json", data=json.dumps(user1))
        self.assertEqual(login_response.json, {
                         "error": "User jb doesn't exist"})

    def test_post_question_successfully(self):
        response = self.app.post('{}auth/signup'.format(BASE_URL),
                                 content_type="application/json", data=json.dumps(user1))
        self.assertEqual(response.json, {"msg": "success!"})
        self.assertEqual(response.status_code, 201)

        login_response = self.app.post(
            '{}auth/login'.format(BASE_URL), content_type="application/json", data=json.dumps(user1))
        self.assertEqual(login_response.status_code, 200)

        login_res = login_response.json
        token = login_res['Token']
        submit_question = self.app.post('{}questions'.format(BASE_URL), content_type="application/json",
                                        data=json.dumps(question1), headers={'Authorization': 'Bearer {}'.format(token)})
        self.assertEqual(submit_question.status_code, 201)

    def test_post_an_answer_successfully(self):
        response_acc = self.app.post(
            '{}auth/signup'.format(BASE_URL), content_type="application/json", data=json.dumps(user1))
        self.assertEqual(response_acc.status_code, 201)

        login_response = self.app.post(
            '{}auth/login'.format(BASE_URL), content_type="application/json", data=json.dumps(user1))
        login_res = login_response.json
        token = login_res['Token']
        create_question = self.app.post('{}questions'.format(BASE_URL), content_type="application/json",
                                        data=json.dumps(question1), headers={'Authorization': 'Bearer {}'.format(token)})
        self.assertEqual(create_question.status_code, 201)

        add_an_answer = self.app.post('{}questions/1/answers'.format(BASE_URL), content_type="application/json",
                                      data=json.dumps(answer1), headers={'Authorization': 'Bearer {}'.format(token)})
        self.assertEqual(add_an_answer.status_code, 201)

    def tearDown(self):
        sql_query_subscribers = "DROP TABLE IF EXISTS subscribers"
        sql_query_questions = "DROP TABLE IF EXISTS questions"
        sql_query_answers = "DROP TABLE IF EXISTS answers"

        sql_list = [sql_query_subscribers,
                    sql_query_questions, sql_query_answers]
        for query in sql_list:
            self.cur.cursor.execute(query)
