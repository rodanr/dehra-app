from flask_restful import Resource
from flask import request
import json, os, datetime
from werkzeug.utils import secure_filename
from advertisement_management.models.advertisement import AdvertisementModel
from advertisement_management.schemas.advertisement import (
    AdvertisementSchema,
    SearchAdvertisementSchema,
)

# Instances of schema
advertisement_schema = AdvertisementSchema()
search_advertisement_schema = SearchAdvertisementSchema()


class PostAdvertisement(Resource):
    @classmethod
    def post(cls):
        user_id = request.form["user_id"]
        property_type = request.form["property_type"]
        property_address = request.form["property_address"]
        geo_location = request.form["geo_location"]
        room_count = request.form["room_count"]
        price = request.form["price"]
        photo = request.files["photo"]
        description = request.form["description"]
        water_source = request.form["water_source"]
        bathroom = request.form["bathroom"]
        terrace_access = request.form["terrace_access"]
        filename=secure_filename(photo.filename)
        extension = filename.split('.')[-1]
        filename = datetime.datetime.now().strftime("%y%m%d_%H%M%S_%f")
        newfilename = filename+"."+extension
        filelocation = os.path.dirname(os.path.realpath(__file__))+"/uploaded_files/"
        if not os.path.isdir(filelocation):
            os.makedirs(filelocation)
        filename_and_location = os.path.join(filelocation ,newfilename)
        photo.save(filename_and_location)
        advertisement_json = {
            "user_id" : user_id,
            "property_type" : property_type,
            "property_address" : property_address,
            "geo_location" : geo_location,
            "room_count" : room_count,
            "price" : float(price.split(",")[0]),
            "photo" : filename_and_location,
            "description" : description,
            "water_source" : water_source,
            "bathroom" : bathroom,
            "terrace_access" : bool(terrace_access)
        }
        advertisement_json = json.dumps(advertisement_json)
        advertisement_data = advertisement_schema.loads(advertisement_json)
        advertisement = AdvertisementModel(
            advertisement_data["user_id"],
            advertisement_data["property_type"],
            advertisement_data["property_address"],
            advertisement_data["geo_location"],
            advertisement_data["room_count"],
            advertisement_data["price"],
            advertisement_data["photo"],
            advertisement_data["description"],
            advertisement_data["water_source"],
            advertisement_data["bathroom"],
            advertisement_data["terrace_access"],
        )
        advertisement.save_to_db()
        # We can only use the backref now i.e advertisement.user as after putting the user_id foreign key
        # then only flask-sqlalchemy can identify user object using the foreign key as there is no magic
        # and sqlalchemy needs to know the foreign key value and then search in the table for back ref using that foreign key
        print(
            advertisement.user.mobile_number
            + "\n"
            + advertisement.user.username
            + "\n"
            + advertisement.user.email
        )
        return {"message": "Advertisement Successfully added"}, 200


class GetAdvertisementLists(Resource):
    @classmethod
    def get(cls, location_to_search):
        # location_to_search_json = request.get_json()
        # location_to_search_data = search_advertisement_schema.load(location_to_search_json)
        # location_to_search = location_to_search_data['location_to_search']
        # Returns list of AdvertisementModel Object so, we cannot pass it directly and needs to be \
        # converted into json or dictionary or simple list
        advertisement_list = AdvertisementModel.get_advertisement_lists_by_location(
            location_to_search
        )
        # print(location_to_search)
        # generating dictionary
        advertisements_found = []
        for advertisement in advertisement_list:
            advertisements_found.append(
                {
                    "advertisement_id": advertisement.id,
                    "price": advertisement.price,
                    "property_type": advertisement.property_type,
                    "property_address": advertisement.property_address,
                    "photo": advertisement.photo,
                    "room_count": advertisement.room_count,
                    "user_id": advertisement.user_id,
                    "username": advertisement.user.username,
                }
            )

        return {"advertisement_list": advertisements_found}, 200


class GetSingleAdvertisement(Resource):
    @classmethod
    def get(cls, advertisement_id):
        advertisement = AdvertisementModel.find_by_id(advertisement_id)
        return {
            "user_id": advertisement.user_id,
            "property_type": advertisement.property_type,
            "property_address": advertisement.property_address,
            "geo_location": advertisement.geo_location,
            "room_count": advertisement.room_count,
            "price": advertisement.price,
            "photo": advertisement.photo,
            "description": advertisement.description,
            "water_source": advertisement.water_source,
            "bathroom": advertisement.bathroom,
            "terrace_access": advertisement.terrace_access,
            "username": advertisement.user.username,
        }, 200


class GetAdvertisementListsByUserId(Resource):
    @classmethod
    def get(cls, user_id):
        advertisement_list = AdvertisementModel.find_by_user_id(user_id)
        advertisements_found = []
        for advertisement in advertisement_list:
            advertisements_found.append(
                {
                    "advertisement_id": advertisement.id,
                    "price": advertisement.price,
                    "property_type": advertisement.property_type,
                    "property_address": advertisement.property_address,
                    "photo": advertisement.photo,
                    "room_count": advertisement.room_count,
                    "user_id": advertisement.user_id,
                    "username": advertisement.user.username,
                }
            )
        return {"advertisement_list": advertisements_found}, 200
