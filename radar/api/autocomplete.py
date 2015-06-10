from flask import current_app, request, jsonify
from flask.ext.restful import Resource, reqparse, marshal
from flask.ext.login import login_required
from radar.models import db, EveType, SolarSystem
from radar.api.serializers import system_fields
from radar.app import csrf


class SystemAutoCompleteResource(Resource):

    decorators = [csrf.exempt, login_required]

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('query', type=str, required=True)
        args = parser.parse_args()
        query = args['query']
        if len(query) < 3:
            return jsonify({'error': 'The search query needs to be > 3 characters'}, 400)
        return marshal(SolarSystem.query.filter(SolarSystem.name.ilike('%{}%'.format(query))).limit(10).all(), system_fields)


class EveTypeAutoCompleteResource(Resource):

    decorators = [csrf.exempt, login_required]

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('query', type=str, required=True)
        args = parser.parse_args()
        query = args['query']
        if len(query) < 3:
            return jsonify({'error': 'The search query needs to be > 3 characters'}, 400)
        return marshal(EveType.query.filter(EveType.name.ilike('%{}%'.format(query))).limit(10).all(), system_fields)

