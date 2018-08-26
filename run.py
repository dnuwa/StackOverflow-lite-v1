from app.api import app, api, Users, AuthLogin, Questions, QuestionByID, Answers, FetchAllAnswers, EditAnswer, MarkAnswerPreferred
from flask_jwt_extended import JWTManager

app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
jwt = JWTManager(app)

api.add_resource(Users, '/auth/signup')
api.add_resource(AuthLogin, '/auth/login')
api.add_resource(Questions, '/questions')
api.add_resource(QuestionByID, '/questions/<questionId>')
api.add_resource(Answers, '/questions/<questionId>/answers')
api.add_resource(EditAnswer, '/questions/<questionId>/answers/<answerId>')
api.add_resource(MarkAnswerPreferred, '/question/<questionId>/answers/<answerId>')


api.add_resource(FetchAllAnswers, '/questions/answers')

if __name__ == '__main__':
    app.run(debug=True)
