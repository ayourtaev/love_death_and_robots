from marshmallow import (
    Schema,
    fields)


class LandmarkSerializer(Schema):
    coordinate = fields.String(required=True)
    name = fields.String(required=True)
