from flask_jwt import jwt_required
from flask_restful import reqparse, Resource

from models.store import StoreModel


class Store(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        'name',
        type=str,
        required=True,
        help='This field cannot be blank'
    )

    @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return {'store': store.json()}, 200

        return {'message': 'Store not found'}, 404

    @jwt_required()
    def post(self):
        data = self.parser.parse_args()
        if StoreModel.find_by_name(data['name']):
            return {'message': 'Store with name {} already exists'.format(data['name'])}, 409

        store = StoreModel(**data)
        store.save_to_db()
        return {'message': 'Store created'}, 201

    @jwt_required()
    def put(self, name):
        data = self.parser.parse_args()
        store = StoreModel.find_by_name(name)
        if store:
            store.name = data['name']
            status = 200
        else:
            store = StoreModel(data['name'])
            status = 201

        store.save_to_db()
        return store.json(), status

    @jwt_required()
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {'message': 'Store deleted'}, 200

        return {'message': 'Store not found'}, 404


class StoreList(Resource):

    @jwt_required()
    def get(self):
        stores = StoreModel.query.all()
        if stores:
            return {'stores': [store.json() for store in stores]}, 200

        return {'message': 'No stores'}, 404
