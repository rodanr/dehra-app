from ma import ma
from advertisement_management.models.advertisement import AdvertisementModel, ImageModel


class AdvertisementSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AdvertisementModel
        dump_only = ("id",)
        # enables to load foreign key value
        include_fk = True


class SearchAdvertisementSchema(ma.Schema):
    class Meta:
        fields = ("location_to_search",)


class ImageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ImageModel
        dump_only = ("advertisement_id",)
        include_fk = True
