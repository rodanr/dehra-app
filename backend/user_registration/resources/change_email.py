from user_registration.models.user import UserModel
from flask_restful import Resource, reqparse


class UserEmail(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank"
                        )
    parser.add_argument('newemail',
                        type=str,
                        required=True,
                        help="This field cannot be blank"
                        )

    def post(self):
        data = UserEmail.parser.parse_args()
        user = UserModel.find_by_username(data['username'])
        if user is None:
            return{'message': 'User doesn\'t exist'}, 400  # Bad Request
        if user.password != data['password']:
            return{'messsage': 'Password is Incorrect'}, 401  # Unauthorized

        user.email = data['newemail']
        user.save_to_db()
        return{'message': 'Email Changed Successfully'}, 200  # Ok
