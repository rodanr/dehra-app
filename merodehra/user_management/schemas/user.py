from ma import ma
from user_management.models.user import UserModel


class UserSignUpSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UserModel
        load_only = ("password",)
        dump_only = ("id",)

    # This auto fielding code can be removed by putting ma.SQLAlchemyAutoSchema instead of ma.SQLAlchemySchema
    id = ma.auto_field()
    username = ma.auto_field()
    email = ma.auto_field()
    mobile_number = ma.auto_field()
    password = ma.auto_field()


class UserLogInSchema(ma.Schema):
    class Meta:
        fields = ("username", "password")
        load_only = ("password",)


class UserPasswordChangeSchema(ma.Schema):
    class Meta:
        fields = ("username", "old_password", "new_password")
        load_only = ("old_password", "new_password")


class UserEmailChange(ma.Schema):
    class Meta:
        fields = ("username", "password", "new_email")
        load_only = ("password",)


class UserMobileNumberChange(ma.Schema):
    class Meta:
        fields = ("username", "password", "new_mobile_number")
        load_only = ("password",)
