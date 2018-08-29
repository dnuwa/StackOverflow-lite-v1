import unittest
import json
from models.dbmodels import DatabaseAccess
from app.api import app, api
from data import user1, user2, user3, user4, user5, user6, user7, question1
from run import api

BASE_URL = '/api/v1/'


class TestClass(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.cur = DatabaseAccess()
        self.cur.create_table_subscribers()
        self.cur.create_table_answer()
        self.cur.create_table_questions()

    def test_user_added_successfully(self):
        response = self.app.post('/api/v1/auth/signup', content_type = "application/json", data =json.dumps(user1))
        self.assertEqual(response.json, {"msg": "success!"})
        self.assertEqual(response.status_code, 201)

    # test user signup
    def test_user_attempts_already_used_name(self):
        response = self.app.post('{}auth/signup'.format(BASE_URL),
                                 content_type="application/json", data=json.dumps(user1))
        self.assertEqual(
            response.json, {'msg': 'This display_name is taken, choose another'})
        self.assertEqual(response.status_code, 401)

    def test_user_attempts_missing_fields(self):
        response = self.app.post('{}auth/signup'.format(BASE_URL),
                                 content_type="application/json", data=json.dumps(user3))
        self.assertEqual(response.status_code, 400)
        self.assertNotIn("display_name", user3)

    def test_all_fields_are_filled(self):
        response = self.app.post('{}auth/signup'.format(BASE_URL),
                                 content_type="application/json", data=json.dumps(user4))
        self.assertEqual(response.status_code, 400)

    def test_user_attempts_already_used_email(self):
        response = self.app.post('{}auth/signup'.format(BASE_URL),
                                 content_type="application/json", data=json.dumps(user5))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json, {"msg": "An account with this email exists"})

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

    def test_user_logsIn_succefully(self):
        login_response = self.app.post(
            '{}auth/login'.format(BASE_URL), content_type="application/json", data=json.dumps(user1))
        self.assertEqual(login_response.status_code, 200)

    def test_unregistered_user_login(self):
        login_response = self.app.post(
            '{}auth/login'.format(BASE_URL), content_type="application/json", data=json.dumps(user2))
        self.assertEqual(login_response.json, {
                         "error": "User bugingo doesn't exist"})
        self.assertEqual(login_response.status_code, 401)

    def test_user_passes_wrong_password(self):
        login_response = self.app.post(
            '{}auth/login'.format(BASE_URL), content_type="application/json", data=json.dumps(user7))
        self.assertEqual(login_response.json, {
                         'error': 'You have entered a wrong password'})
        self.assertEqual(login_response.status_code, 400)
        


def tearDown(self):
    sql_query_subscribers = "DROP TABLE IF EXISTS subscribers"
    sql_query_questions = "DROP TABLE IF EXISTS questions"
    sql_query_answers = "DROP TABLE IF EXISTS answers"

    sql_list = [sql_query_subscribers, sql_query_questions, sql_query_answers]
    for query in sql_list:
        self.cur.cursor.execute(query)
