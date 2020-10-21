from flask import Flask
from flask_restful import Api
from db import db
from ma import ma
from user_management.resources.user import (
    UserSignUp,
    UserLogin,
    UserPasswordChange,
    UserEmailChange,
    UserMobileNumberChange,
)
from advertisement_management.resources.advertisement import (
    PostAdvertisement,
    GetAdvertisementLists,
    GetSingleAdvertisement,
    GetAdvertisementListsByUserId,
)

HEROKU_POSTGRES_URL = "postgres://aculeptjtivfxw:f59a97935e203b20e111d3494275b3a2ba3285a09b5aeb67fd43799a80a5e997@ec2-54-164-134-207.compute-1.amazonaws.com:5432/dfsk7g8tc3sgvn"
TEST_DATABASE_SQL_LITE_URL = "sqlite:///data.db"
app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = HEROKU_POSTGRES_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
ma.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()


# user_management api list
api.add_resource(UserSignUp, "/signup")
api.add_resource(UserLogin, "/login")
api.add_resource(UserPasswordChange, "/change-password")
api.add_resource(UserEmailChange, "/change-email")
api.add_resource(UserMobileNumberChange, "/change-mobile-number")

# advertisement_management api list
api.add_resource(PostAdvertisement, "/advertisement")
api.add_resource(GetAdvertisementLists, "/search/<string:location_to_search>")
api.add_resource(GetSingleAdvertisement, "/advertisement/<int:advertisement_id>")
api.add_resource(GetAdvertisementListsByUserId, "/advertisement/user/<int:user_id>")
if __name__ == "__main__":
    app.run(port=5000, debug=True)
