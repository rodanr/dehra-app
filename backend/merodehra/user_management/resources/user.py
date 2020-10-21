from flask_restful import Resource
from flask import request
from werkzeug.security import check_password_hash, generate_password_hash
from user_management.models.user import UserModel
from user_management.schemas.user import (
    UserSignUpSchema,
    UserLogInSchema,
    UserPasswordChangeSchema,
    UserEmailChange,
    UserMobileNumberChange,
)

# Instances of schemas
user_sign_up_schema = UserSignUpSchema()
user_log_in_schema = UserLogInSchema()
user_password_change_schema = UserPasswordChangeSchema()
user_email_change_schema = UserEmailChange()
user_mobile_number_change_schema = UserMobileNumberChange()

# Messages
USER_ALREADY_EXISTS = "A user with this username already exists."
CREATED_SUCCESSFULLY = "User created successfully."
USER_NOT_FOUND = "User doesn't exist"
USER_DELETED = "User deleted."
INVALID_CREDENTIALS = "Invalid credentials!"
PASSWORD_CHANGED_SUCCESSFULLY = "Password Changed Successfully"
LOGGED_IN_SUCCESSFULLY = "Logged In Successfully"
INCORRECT_OLD_PASSWORD = "Incorrect Old Password"
EMAIL_CHANGED_SUCCESSFULLY = "Email Changed Successfully"
MOBILE_NUMBER_CHANGED_SUCCESSFULLY = "Mobile Number Changed Successfully"


class UserSignUp(Resource):
    @classmethod
    def post(cls):
        user_sign_up_json = request.get_json()
        user_data_for_sign_up = user_sign_up_schema.load(user_sign_up_json)
        user = UserModel(
            user_data_for_sign_up["username"],
            user_data_for_sign_up["email"],
            user_data_for_sign_up["mobile_number"],
            generate_password_hash(user_data_for_sign_up["password"]),
        )
        if UserModel.find_by_username(user.username):
            return {"message": USER_ALREADY_EXISTS}, 400
        if UserModel.find_by_mobile_number(user.mobile_number):
            return {"message": "Mobile Number Already Registered"}, 400
        if UserModel.find_by_email(user.email):
            return {"message": "Email Already Registered"}, 400
        user.save_to_db()
        return {"message": CREATED_SUCCESSFULLY}, 200


class UserLogin(Resource):
    @classmethod
    def post(cls):
        user_log_in_json = request.get_json()
        user_data = user_log_in_schema.load(user_log_in_json)

        user = UserModel.find_by_username(user_data["username"])
        if user and check_password_hash(user.password, user_data["password"]):
            return {
                "message": LOGGED_IN_SUCCESSFULLY,
                "user_id": user.id,
                "username": user.username,
                "email": user.email,
                "mobile_number": user.mobile_number,
            }, 200
        return {"message": INVALID_CREDENTIALS}, 400


class UserPasswordChange(Resource):
    @classmethod
    def post(cls):
        user_password_change_json = request.get_json()
        user_data_for_password_change = user_password_change_schema.load(
            user_password_change_json
        )
        user = UserModel.find_by_username(user_data_for_password_change["username"])
        if not user:
            return {"message": USER_NOT_FOUND}, 400  # Bad Request
        if user.password and check_password_hash(
            user.password, user_data_for_password_change["old_password"]
        ):
            user.password = generate_password_hash(
                user_data_for_password_change["new_password"]
            )
            user.save_to_db()
            return {"message": PASSWORD_CHANGED_SUCCESSFULLY}, 200
        return {"message": INCORRECT_OLD_PASSWORD}


class UserEmailChange(Resource):
    @classmethod
    def post(cls):
        user_email_change_json = request.get_json()
        user_data_for_email_change = user_email_change_schema.load(
            user_email_change_json
        )
        user = UserModel.find_by_username(user_data_for_email_change["username"])
        if not user:
            return {"message": USER_NOT_FOUND}, 400  # Bad Request
        if user.password and check_password_hash(
            user.password, user_data_for_email_change["password"]
        ):
            user.email = user_data_for_email_change["new_email"]
            user.save_to_db()
            return {"message": EMAIL_CHANGED_SUCCESSFULLY}, 200
        return {"message": INVALID_CREDENTIALS}, 400


class UserMobileNumberChange(Resource):
    @classmethod
    def post(cls):
        user_mobile_number_change_json = request.get_json()
        user_data_for_mobile_number_change = user_mobile_number_change_schema.load(
            user_mobile_number_change_json
        )
        user = UserModel.find_by_username(
            user_data_for_mobile_number_change["username"]
        )
        if not user:
            return {"message": USER_NOT_FOUND}, 400  # Bad Request
        if user.password and check_password_hash(
            user.password, user_data_for_mobile_number_change["password"]
        ):
            user.mobile_number = user_data_for_mobile_number_change["new_mobile_number"]
            user.save_to_db()
            return {"message": MOBILE_NUMBER_CHANGED_SUCCESSFULLY}, 200
        return {"message": INVALID_CREDENTIALS}, 400
