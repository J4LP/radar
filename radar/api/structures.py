import uuid
from flask import current_app, request
from flask.ext.restful import Resource, reqparse, marshal
from flask.ext.login import login_required, current_user
from radar.models import db, Structure, Scan, EveType, SolarSystem
from radar.api.exceptions import InvalidUUIDError, InvalidSystemError, InvalidEveTypeError
from radar.api.serializers import structure_fields
from radar.api.parsers import structure_parser
from radar.app import csrf


class StructureListResource(Resource):

    decorators = [csrf.exempt, login_required]

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, default=1)
        parser.add_argument('limit', type=int, default=20)
        args = parser.parse_args()
        pagination = Structure.query.order_by(Structure.created_on.desc()).paginate(args.get('page'), args.get('limit'))
        return {
            'num_results': pagination.total,
            'page': pagination.page,
            'num_pages': pagination.pages,
            'objects': marshal(pagination.items, structure_fields)
        }

    @staticmethod
    def post():
        args = structure_parser.parse_args()
        eve_type = EveType.query.filter(EveType.name.ilike(args['type'])).first()
        if not eve_type:
            raise InvalidEveTypeError
        system = SolarSystem.query.filter(SolarSystem.name.ilike(args['system'])).first()
        if not system:
            raise InvalidSystemError
        structure = Structure(planet=args['planet'], corporation=args['corporation'], alliance=args['alliance'], eve_type=eve_type, system=system, added_by=current_user)
        if args.get('scan'):
            structure.scan = Scan(content=args['scan'], added_by=current_user)
        db.session.add(structure)
        db.session.commit()
        return marshal(structure, structure_fields)


class StructureResource(Resource):

    decorators = [csrf.exempt, login_required]

    def _get_structure(self, structure_id):
        try:
            _ = uuid.UUID(structure_id, version=4)
            return Structure.query.get_or_404(structure_id)
        except ValueError:
            raise InvalidUUIDError

    def get(self, structure_id):
        return marshal(self._get_structure(structure_id), structure_fields)


class StructureScanResource(Resource):

    decorators = [csrf.exempt, login_required]

    def _get_structure(self, structure_id):
        try:
            _ = uuid.UUID(structure_id, version=4)
            return Structure.query.get_or_404(structure_id)
        except ValueError:
            raise InvalidUUIDError

    def put(self, structure_id):
        structure = self._get_structure(structure_id)
        parser = reqparse.RequestParser()
        parser.add_argument('scan', type=str, required=True)
        args = parser.parse_args()
        structure.scan = Scan(content=args['scan'], added_by=current_user)
        db.session.add(structure)
        db.session.commit()
        return 204




