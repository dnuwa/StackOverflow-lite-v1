from flask import Flask, request
from models.dbmodels import DatabaseAccess
from flask_restful import Resource, Api
from werkzeug.security import generate_password_hash, check_password_hash
import re
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)
api = Api(app, prefix="/api/v1")


class Users(Resource):
    def __init__(self, display_name=None, email=None, password=None):
        self.display_name = display_name
        self.email = email
        self.password = password

    def post(self):
        new_user = DatabaseAccess()
        new_user.create_table_subscribers()

        data = request.get_json()
        try:
            display_name = data['display_name'].strip()
            email = data['email'].strip()
            #password = data['password'].strip()
            hashed_password = generate_password_hash(
                data['password'].strip(), method='sha256')

            if display_name == "" or hashed_password == "":
                return {'error': 'ensure all feilds are field correctlty'}, 400

            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                return {'error': 'Invalid email address'}, 400

            check_name = new_user.no_name_duplicates(display_name)
            check_email = new_user.no_email_duplicates(email)
            for user_name in check_name:
                if user_name['display_name'] == display_name:
                    return {'msg': 'This display_name is taken, choose another'}, 401
            for user_email in check_email:
                if user_email['email'] == email:
                    return {'msg': 'An account with this email exists'}, 401

            new_user.add_new_subscriber(display_name, email, hashed_password)
            print("user created")
            return {'msg': 'success!'}, 201

        except KeyError as e:
            return {'error': str(e)+",missed out some info, check the keys too"}, 400

    def get(self):
        all_subscribers = DatabaseAccess()
        subscribers = all_subscribers.query_all_subscribers()
        return {'subscribers': subscribers}, 200


class AuthLogin(Resource):
    def post(self):
        try:
            data = request.get_json()
            display_name = data['display_name'].strip()
            password = data['password'].strip()

            userobj = DatabaseAccess()
            current_user = userobj.no_name_duplicates(display_name)

            if not current_user:
                return {'error': 'User {} doesn\'t exist'.format(display_name)}, 401

            for user in current_user:
                if user['display_name'] == display_name and check_password_hash(user['password'], password):
                    access_token = create_access_token(identity=user['user_id'])
                    return {
                        'msg': 'Logged in as {}'.format(user['display_name']),
                        'Token': access_token
                        }, 200

                else:
                    return {'error': 'You have entered a wrong password'}, 400

        except Exception as err:
            return {'error': str(err)+"field missing!"}, 401

class Questions(Resource):
   
    @jwt_required
    def post(self):
        new_qn = DatabaseAccess()
        new_qn.create_table_questions()
        qn_info = request.get_json()

        try:
            question = qn_info['question'].strip()
            current_user_id = get_jwt_identity()

            if question == "":
                return {'error':'Please add a question'}, 400
   
            new_qn.post_a_question(current_user_id, question)
            return {'msg':'Question has successfully added'}, 201

        except Exception as err:
            return {'error': str(err)+ "field missing!"}, 401

    @jwt_required
    def get(self):
        fetch_all = DatabaseAccess()
        all_questions = fetch_all.retrieve_all()
        return {'Asked Questions': all_questions}, 200
