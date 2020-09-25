from flask import Flask
from flask_restful import Api
from user_registration.resources.user import UserRegister
from user_registration.resources.change_email import UserEmail
from flask_jwt import JWT
from user_registration.security import authenticate, identity

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'postgres://aculeptjtivfxw:f59a97935e203b20e111d3494275b3a2ba3285a09b5aeb67fd43799a80a5e997@ec2-54-164-134-207.compute-1.amazonaws.com:5432/dfsk7g8tc3sgvn'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)
app.secret_key = 'rodan0818'

jwt = JWT(app, authenticate, identity)  # lies in /auth


@app.before_first_request
def create_tables():
    db.create_all()


# Resources for User Registration
api.add_resource(UserRegister, '/user')
api.add_resource(UserEmail, '/user/change-email')

if __name__ == '__main__':
    from db import db

    db.init_app(app)  # constructing an instance
    app.run(port=5000, debug=True)
