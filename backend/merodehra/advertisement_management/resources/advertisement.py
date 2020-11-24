import datetime
import json
import os
from flask import request, make_response, render_template
from sqlalchemy import desc
from flask_restful import Resource
from werkzeug.utils import secure_filename

from advertisement_management.models.advertisement import AdvertisementModel, ImageModel, ChatUserModel, \
    ChatMessageModel
from advertisement_management.schemas.advertisement import (
    AdvertisementSchema,
    SearchAdvertisementSchema,
    ImageSchema,
    ChatUserSchema,
    ChatMessageSchema
)

# Instances of schema
advertisement_schema = AdvertisementSchema()
search_advertisement_schema = SearchAdvertisementSchema()
image_schema = ImageSchema()
chat_user_schema = ChatUserSchema()
chat_message_schema = ChatMessageSchema()

ALLOWED_EXTENSION = set(['png', 'jpg', 'jpeg', 'gif'])


# Function to check weather the file to be uploaded is an image or not
def allowed_file(filename):
    ext = filename.split('.')[-1]
    # if ext.lower() in ALLOWED_EXTENSION:
    #     print(True)
    #
    # return True

    # returns TRUE if the extension is in the ALLOWED_EXTENSION
    return '.' in filename and ext.lower() in ALLOWED_EXTENSION


class PostAdvertisement(Resource):
    @classmethod
    def post(cls):
        user_id = request.form["user_id"]
        property_type = request.form["property_type"]
        property_address = request.form["property_address"]
        geo_location = request.form["geo_location"]
        room_count = request.form["room_count"]
        price = request.form["price"]
        # photo = request.files["photo"]
        description = request.form["description"]
        water_source = request.form["water_source"]
        bathroom = request.form["bathroom"]
        terrace_access = request.form["terrace_access"]
        # filename=secure_filename(photo.filename)
        # extension = filename.split('.')[-1]
        # filename = datetime.datetime.now().strftime("%y%m%d_%H%M%S_%f")
        # newfilename = filename+"."+extension
        # filelocation = os.path.dirname(os.path.realpath(__file__))+"/uploaded_files/"
        # if not os.path.isdir(filelocation):
        #     os.makedirs(filelocation)
        # filename_and_location = os.path.join(filelocation ,newfilename)
        # photo.save(filename_and_location)

        # image upload section
        uploaded_images = request.files.getlist("photos[]")
        print(uploaded_images)
        img = []
        for image in uploaded_images:
            if image and allowed_file(image.filename):
                image_name = secure_filename(image.filename)
                # print(image_name)
                extension = image_name.split('.')[-1]
                image_name = datetime.datetime.now().strftime("%y%m%d_%H%M%S_%f")
                newfilename = image_name + "." + extension
                IMAGE_UPLOAD_FOLDER = os.path.dirname(os.path.realpath(__file__)) + "/pictures/"
                if not os.path.isdir(IMAGE_UPLOAD_FOLDER):
                    os.makedirs(IMAGE_UPLOAD_FOLDER)
                image_path = os.path.join(IMAGE_UPLOAD_FOLDER, newfilename)
                img.append(image_name)
                # print(image_path)
                image.save(image_path)
        # print(img)

        advertisement_json = {
            "user_id": user_id,
            "property_type": property_type,
            "property_address": property_address,
            "geo_location": geo_location,
            "room_count": room_count,
            "price": float(price.split(",")[0]),
            "description": description,
            "water_source": water_source,
            "bathroom": bathroom,
            "terrace_access": bool(terrace_access),
            "image": {
                "advertisement_id": user_id,
                "image_1": img[0],
                "image_2": img[1],
                "image_3": img[2],
                "image_4": img[3],
                "image_5": img[4],
                "image_6": img[5],
                "image_7": img[6]
            }
        }

        image_json = json.dumps(advertisement_json)
        image_data = image_schema.load(image_json)
        ad_image = ImageModel(
            image_data["image"]["advertisement_id"],
            image_data["image"]["image_1"],
            image_data["image"]["image_2"],
            image_data["image"]["image_3"],
            image_data["image"]["image_4"],
            image_data["image"]["image_5"],
            image_data["image"]["image_6"],
            image_data["image"]["image_7"],
        )
        ad_image.save_to_db()

        advertisement_json = json.dumps(advertisement_json)
        advertisement_data = advertisement_schema.loads(advertisement_json)
        advertisement = AdvertisementModel(
            advertisement_data["user_id"],
            advertisement_data["property_type"],
            advertisement_data["property_address"],
            advertisement_data["geo_location"],
            advertisement_data["room_count"],
            advertisement_data["price"],
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
                    "room_count": advertisement.room_count,
                    "user_id": advertisement.user_id,
                    "username": advertisement.user.username,
                }
            )

        return {"advertisement_list": advertisements_found}, 200

    @classmethod
    def get(cls):
        return make_response(render_template('form.html'))


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
                    "room_count": advertisement.room_count,
                    "user_id": advertisement.user_id,
                    "username": advertisement.user.username,
                }
            )
        return {"advertisement_list": advertisements_found}, 200


class PostChatId(Resource):
    @classmethod
    def post(cls):
        chat_id_json = request.get_json()
        chat_id_data = chat_user_schema.load(chat_id_json)
        if ChatUserModel.find_owner_id(chat_id_data["owner_id"]) and ChatUserModel.find_renter_id(
                chat_id_data["renter_id"]):
            user_id = ChatUserModel.get_id(chat_id_data["owner_id"], chat_id_data["renter_id"])
            return {"chat_user_id": user_id}
        else:
            chat_id = ChatUserModel(
                chat_id_data["owner_id"],
                chat_id_data["renter_id"],
            )
            chat_id.save_to_db()
            return {"message": "Successfully add chat id"}


class ChatMessage(Resource):
    @classmethod
    def post(cls):
        chat_message_json = request.get_json()
        chat_message_data = chat_message_schema.load(chat_message_json)
        chat_message = ChatMessageModel(
            chat_message_data["message"],
            chat_message_data["room_id"]
        )
        chat_message.save_to_db()
        return {"message": "successfully added"}

    @classmethod
    def get(cls, room_id):
        message_list = ChatMessageModel.order_message_dec(room_id)
        message_found = []
        for message in message_list:
            message_found.append(
                {
                    "message": message.message,
                }
            )
        print(message_found)
        return message_found
