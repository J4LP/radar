from flask.ext.restful import Api
from .structures import StructureListResource, StructureResource, StructureScanResource
from .autocomplete import EveTypeAutoCompleteResource, SystemAutoCompleteResource

errors = {
    'InvalidUUIDError': {
        'message': 'Invalid model UUID',
        'status': 400
    },
    'InvalidEveTypeError': {
        'message': 'Invalid Eve Type',
        'status': 400
    },
    'InvalidSystemError': {
        'message': 'Invalid System',
        'status': 400
    }
}

api_manager = Api(prefix='/api', errors=errors)
api_manager.add_resource(StructureListResource, '/structures')
api_manager.add_resource(StructureResource, '/structures/<structure_id>')
api_manager.add_resource(StructureScanResource, '/structures/<structure_id>/scan')
api_manager.add_resource(EveTypeAutoCompleteResource, '/autocomplete/evetypes')
api_manager.add_resource(SystemAutoCompleteResource, '/autocomplete/systems')
