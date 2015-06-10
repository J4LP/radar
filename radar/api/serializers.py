from flask.ext.restful import Resource, fields, marshal_with, marshal, reqparse

class DateTimeField(fields.Raw):
    def format(self, value):
        return value.isoformat()


class UUIDField(fields.Raw):
    def format(self, value):
        return str(value)


class IPField(fields.Raw):
    def format(self, value):
        return str(value)


class EnumField(fields.Raw):
    def format(self, enum):
        return enum.value

user_fields = {
    'id': fields.Integer,
    'user_id': fields.String,
    'main_character': fields.String,
    'corporation': fields.String(attribute=lambda x: x.corporation_name),
    'alliance': fields.String(attribute=lambda x: x.alliance_name)
}

scan_fields = {
    'id': UUIDField,
    'content': fields.String,
    'added_by': fields.Nested(user_fields),
    'created_on': DateTimeField,
    'updated_on': DateTimeField
}

structure_fields = {
    'id': UUIDField,
    'system': fields.String(attribute=lambda x: x.system.name),
    'eve_type': fields.String(attribute=lambda x: x.eve_type.name),
    'planet': fields.String,
    'corporation': fields.String,
    'alliance': fields.String,
    'standing': fields.Integer,
    'status': fields.String,
    'scan': fields.Nested(scan_fields, allow_null=True),
    'added_by': fields.Nested(user_fields, allow_null=True),
    'created_on': DateTimeField,
    'updated_on': DateTimeField,
}

system_fields = {
    'id': fields.Integer,
    'name': fields.String
}
