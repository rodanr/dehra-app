from models.user import UserModel
from flask_restful import Resource, reqparse


class UserRegister(Resource):
    # Parser for new Account
    parser_for_new_account = reqparse.RequestParser()
    parser_for_new_account.add_argument('username',
                                        type=str,
                                        required=True,
                                        help="This field cannot be blank"
                                        )
    parser_for_new_account.add_argument('email',
                                        type=str,
                                        required=True,
                                        help="This field cannot be blank")
    parser_for_new_account.add_argument('password',
                                        type=str,
                                        required=True,
                                        help="This field cannot be blank")
    # Parser to delete account
    parser_to_delete_account = reqparse.RequestParser()
    parser_to_delete_account.add_argument('username',
                                          type=str,
                                          required=True,
                                          help="This field cannot be blank"
                                          )
    parser_to_delete_account.add_argument('password',
                                          type=str,
                                          required=True,
                                          help="This field cannot be blank")
    # Parser to change password or email
    parser_to_change_password = reqparse.RequestParser()
    parser_to_change_password.add_argument('username',
                                           type=str,
                                           required=True,
                                           help="This field cannot be blank"
                                           )
    parser_to_change_password.add_argument('oldpassword',
                                           type=str,
                                           required=True,
                                           help="This field cannot be blank")
    parser_to_change_password.add_argument('newpassword',
                                           type=str,
                                           required=True,
                                           help="This field cannot be blank")

    def post(self):
        data = UserRegister.parser_for_new_account.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        user = UserModel(data['username'], data['email'], data['password'])
        user.save_to_db()
        return {"message": "User created successfully."}, 201

    def delete(self):
        data = UserRegister.parser_to_delete_account.parse_args()
        user_to_delete = UserModel.find_by_username(data['username'])
        if user_to_delete is None:
            return {'message': 'User doesn\'t exist'}
        if user_to_delete.password != data['password']:
            return {'message': 'Password is incorrect'}
        user_to_delete.delete_from_db()
        return {'message': 'User deleted successfully'}

    def put(self):
        data = UserRegister.parser_to_change_password.parse_args()
        user = UserModel.find_by_username(data['username'])
        if user is None:
            return {'message': 'User doesn\'t exist'}
        if user.password != data['oldpassword']:
            return {'message': 'Incorrect old Password'}
        user.password = data['newpassword']
        user.save_to_db()
        return{'message': 'Password Changed Successfully'}
