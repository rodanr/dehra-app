from db import db


class UserModel(db.Model):
    __tablename__ = 'users'
    # set only one column as primary key otherwise multiple primary key in one table may trouble in sqlite
    # id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    # username can be used as primary key here as every user should have unique username
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    # Mobile numbers are only 10 digit long excluding the country codes
    mobile_number = db.Column(db.String(10), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __init__(self, username, email, mobile_number, password):
        self.username = username
        self.email = email
        self.mobile_number = mobile_number
        self.password = password

    @classmethod
    def find_by_username(cls, username: str) -> "UserModel":
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, user_id: int) -> "UserModel":
        return cls.query.filter_by(user_id=user_id).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
