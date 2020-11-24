from db import db


class AdvertisementModel(db.Model):
    __tablename__ = "advertisements"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )  # user_id who created this advertisement
    property_type = db.Column(db.String(10), nullable=False)  # Either its flat or room
    property_address = db.Column(
        db.String(100), nullable=False
    )  # Property's general address
    geo_location = db.Column(
        db.String(100), nullable=False
    )  # Geographical location of property i.e lat & long
    room_count = db.Column(db.Integer, nullable=False)  # Number of rooms
    price = db.Column(db.Float, nullable=False)  # Price of the property
    photo = db.Column(db.String, nullable=False)
    description = db.Column(
        db.String, nullable=False
    )  # Description about the property owner wants to tell
    water_source = db.Column(db.String(80), nullable=False)  # Like Well, boring or tap
    bathroom = db.Column(db.String(80), nullable=False)  # Shared or Private
    terrace_access = db.Column(db.Boolean, nullable=False)

    def __init__(
        self,
        user_id,
        property_type,
        property_address,
        geo_location,
        room_count,
        price,
        photo,
        description,
        water_source,
        bathroom,
        terrace_access,
    ):
        self.user_id = user_id
        self.property_type = property_type
        self.property_address = property_address
        self.geo_location = geo_location
        self.room_count = room_count
        self.price = price
        self.photo = photo
        self.description = description
        self.water_source = water_source
        self.bathroom = bathroom
        self.terrace_access = terrace_access

    @classmethod
    def get_all_desc(cls, number_needed: int) -> list:
        return cls.query.order_by(cls.id.desc()).limit(number_needed).all()

    @classmethod
    def find_by_id(cls, advertisement_id: int) -> "AdvertisementModel":
        return cls.query.filter_by(id=advertisement_id).first()

    @classmethod
    def find_by_user_id(
        cls, user_id: int
    ) -> list:  # List of AdvertisementModel objects
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def get_advertisement_lists_by_location(cls, location_to_search: str) -> list:
        location_to_search_string = "%{}%".format(location_to_search)
        return cls.query.filter(
            AdvertisementModel.property_address.ilike(location_to_search_string)
        ).all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

class ChatUserModel(db.Model):
    __tablename__ = "chatUser"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    owner_id = db.Column(db.Integer)
    renter_id = db.Column(db.Integer)

    def __init__(self, owner_id, renter_id):
        self.owner_id = owner_id
        self.renter_id = renter_id

    @classmethod
    def find_owner_id(cls, owner_id: int):
        return cls.query.filter_by(owner_id=owner_id)

    @classmethod
    def find_renter_id(cls, renter_id: int):
        return cls.query.filter_by(renter_id=renter_id).first()

    @classmethod
    def get_id(cls, owner_id, renter_id):
        return cls.query.filter_by(owner_id=owner_id, renter_id=renter_id).first().id
    
    @classmethod
    def get_users(cls, id):
        return cls.query.filter_by(id=id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class ChatMessageModel(db.Model):
    __tablename__ = "chatMessage"

    message_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    message = db.Column(db.String(200))
    sent_user = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    room_id = db.Column(db.Integer, db.ForeignKey("chatUser.id"), nullable=False)

    def __init__(self, message, sent_user, room_id):
        self.message = message
        self.sent_user = sent_user
        self.room_id = room_id

    @classmethod
    def order_message_dec(cls, id: int):
        return cls.query.filter_by(room_id=id).order_by(cls.message_id.desc()).all()
    
    @classmethod
    def get_id(cls, id: int):
        return cls.query.filter_by(message_id=id).first().room_id

    @classmethod
    def get_latest_msg(cls, id: int):
        return cls.query.filter_by(room_id=id).order_by(cls.message_id.desc()).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()