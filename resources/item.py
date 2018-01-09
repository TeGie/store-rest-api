from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from sqlalchemy import exc

from models.item import ItemModel


class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help='This field cannot be blank'
    )
    parser.add_argument(
        'name',
        type=str,
        required=True,
        help='This field cannot be blank'
    )
    parser.add_argument(
        'store_id',
        type=int,
        required=True,
        help='This field cannot be blank'
    )

    @jwt_required()
    def get(self, name, store_id):
        item = ItemModel.find_by_name_and_store_id(name, store_id)
        if item:
            return {'item': item.json()}, 200

        return {'message': 'Item not found'}, 404

    @jwt_required()
    def post(self):
        data = self.parser.parse_args()

        if ItemModel.find_by_name_and_store_id(data['name'], data['store_id']):
            return {'message': 'Item with name {} in store id {} already exists'.format(
                data['name'], data['store_id']
            )}, 409

        item = ItemModel(**data)
        try:
            item.save_to_db()
        except exc.SQLAlchemyError:
            return {'message': 'An error occurred while saving to database'}

        return {'message': 'Item created'}, 201

    @jwt_required()
    def put(self):
        data = self.parser.parse_args()

        item = ItemModel.find_by_name_and_store_id(data['name'], data['store_id'])

        if item:
            item.price = data['price']
            status = 200
        else:
            item = ItemModel(**data)
            status = 201

        try:
            item.save_to_db()
        except exc.SQLAlchemyError:
            return {'message': 'An error occurred while saving to database'}

        return item.json(), status

    @jwt_required()
    def delete(self, name, store_id):
        item = ItemModel.find_by_name_and_store_id(name, store_id)
        if item:
            item.delete_from_db()
            return {'message': 'Item deleted'}, 200

        return {'message': 'Item not found'}, 404


class ItemList(Resource):

    @jwt_required()
    def get(self):
        items = ItemModel.query.all()
        if items:
            return {'items': [item.json() for item in items]}, 200

        return {'message': 'No items'}, 404
