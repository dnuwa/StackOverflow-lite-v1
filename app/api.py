from flask import Flask, request
from models.dbmodels import DatabaseAccess
from flask_restful import Resource, Api
from werkzeug.security import generate_password_hash, check_password_hash
import re

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
            hashed_password = generate_password_hash(data['password'].strip(), method='sha256')

            if display_name == "" or hashed_password == "":
                return {'error': 'ensure all feilds are field correctlty'}, 400

            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                return {'error': 'Invalid email address'}, 400

            check_name = new_user.no_name_duplicates(display_name)
            check_email = new_user.no_email_duplicates(email)
            for user_name in check_name:            
                if user_name['display_name'] == display_name:
                    return {'msg':'This display_name is taken, choose another'}, 401
            for user_email in check_email:
                if user_email['email'] == email:
                    return {'msg':'An account with this email exists'}, 401

            new_user.add_new_subscriber(display_name, email, hashed_password)        
            print("user created")
            return {'msg':'success!'}, 201

        except KeyError as e:
            return {'error': str(e)+",missed out some info, check the keys too"}, 400

    def get(self):
        all_subscribers = DatabaseAccess()
        subscribers = all_subscribers.query_all_subscribers()
        return {'subscribers': subscribers}, 200
