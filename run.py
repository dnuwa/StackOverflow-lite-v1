from app.api import app, api, Users, AuthLogin, Questions
from flask_jwt_extended import JWTManager

app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
jwt = JWTManager(app)

api.add_resource(Users, '/auth/signup')
api.add_resource(AuthLogin, '/auth/login')
api.add_resource(Questions, '/questions')

if __name__ == '__main__':
    app.run(debug=True)