from db import db
from sqlalchemy import desc


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
        self.description = description
        self.water_source = water_source
        self.bathroom = bathroom
        self.terrace_access = terrace_access

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


class ImageModel(db.Model):
    __tablename__ = "images"

    advertisement_id = db.Column(db.Integer, db.ForeignKey("advertisements.id"), primary_key=True, nullable=False)
    link_1 = db.Column(db.String)
    link_2 = db.Column(db.String)
    link_3 = db.Column(db.String)
    link_4 = db.Column(db.String)
    link_5 = db.Column(db.String)
    link_6 = db.Column(db.String)
    link_7 = db.Column(db.String)

    def __init__(self, advertisement_id, link_1, link_2, link_3, link_4, link_5, link_6, link_7):
        self.advertisement_id = advertisement_id
        self.link_1 = link_1
        self.link_2 = link_2
        self.link_3 = link_3
        self.link_4 = link_4
        self.link_5 = link_5
        self.link_6 = link_6
        self.link_7 = link_7

    def save_to_db(self):
        db.session.add(self)
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
        return cls.query.filter_by(owner_id=owner_id).first()

    @classmethod
    def find_renter_id(cls, renter_id: int):
        return cls.query.filter_by(renter_id=renter_id).first()

    @classmethod
    def get_id(cls, owner_id, renter_id):
        return cls.query.filter_by(owner_id=owner_id, renter_id=renter_id).first().id

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class ChatMessageModel(db.Model):
    __tablename__ = "chatMessage"

    message_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    message = db.Column(db.String())
    room_id = db.Column(db.Integer, db.ForeignKey("chatUser.id"), nullable=False)

    def __init__(self, message, room_id):
        self.message = message
        self.room_id = room_id

    @classmethod
    def order_message_dec(cls, id: int):
        return cls.query.filter_by(room_id=id).order_by(cls.message_id.desc()).all()

    @classmethod
    def get_room_id(cls, id: int):
        return cls.query.filter_by(message_id=id).first().room_id

    @classmethod
    def get_latest_msg(cls, id: int):
        return cls.query.filter_by(room_id=id).order_by(cls.message_id.desc()).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
