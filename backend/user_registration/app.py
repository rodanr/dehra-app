from flask import Flask
from flask_restful import Api
from resources.user import UserRegister
from resources.change_email import UserEmail
from flask_jwt import JWT
from security import authenticate, identity

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)
app.secret_key = 'rodan0818'

jwt = JWT(app, authenticate, identity)  # lies in /auth


@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(UserRegister, '/user')
api.add_resource(UserEmail, '/user/change-email')

if __name__ == '__main__':
    from db import db
    db.init_app(app)  # constructing an instance
    app.run(port=5000, debug=True)
