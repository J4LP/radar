import uuid
from flask.ext.restful.reqparse import RequestParser


def UUIDInput(value):
    val = uuid.UUID(value, version=4)
    return val


structure_parser = RequestParser()

structure_parser.add_argument('system', type=str)
structure_parser.add_argument('planet', type=str)
structure_parser.add_argument('corporation', type=str)
structure_parser.add_argument('alliance', type=str, required=False)
structure_parser.add_argument('type', type=str)
structure_parser.add_argument('scan', type=str, required=False)
