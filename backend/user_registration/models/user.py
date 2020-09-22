from db import db


class UserModel(db.Model):
    # table will be create with this name
    # For this case 'user'
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    mobile_number = db.Column(db.String(10), unique=True, nullable=False)

    def __init__(self, username, email, password, mobile_number):
        self.username = username
        self.email = email
        self.password = password
        self.mobile_number = mobile_number

    def json(self):
        return {'username': self.username, 'email': self.email, 'password': self.password,
                'mobile_number': self.mobile_number}

    @classmethod
    def find_by_username(cls, name):
        return cls.query.filter_by(username=name).first()

    @classmethod
    def find_by_userid(cls, userid):
        return cls.query.filter_by(id=userid).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
