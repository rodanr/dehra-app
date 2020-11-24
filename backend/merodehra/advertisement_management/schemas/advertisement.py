from ma import ma
from advertisement_management.models.advertisement import AdvertisementModel, ChatUserModel, ChatMessageModel


class AdvertisementSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AdvertisementModel
        dump_only = ("id",)
        # enables to load foreign key value
        include_fk = True


class SearchAdvertisementSchema(ma.Schema):
    class Meta:
        fields = ("location_to_search",)

class ChatUserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ChatUserModel
        dump_only = ("id",)
        include_fk = True


class ChatMessageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ChatMessageModel
        dump_only = ("id",)
        include_fk = True