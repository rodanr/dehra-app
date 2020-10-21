from ma import ma
from advertisement_management.models.advertisement import AdvertisementModel


class AdvertisementSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AdvertisementModel
        dump_only = ("id",)
        # enables to load foreign key value
        include_fk = True


class SearchAdvertisementSchema(ma.Schema):
    class Meta:
        fields = ("location_to_search",)
