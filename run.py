from app.api import app, api, Users

api.add_resource(Users, '/auth/signup')

if __name__ == '__main__':
    app.run(debug=True)