from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from models.user import UserModel


class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type=str,
        required=True,
        help='This field cannot be blank'
    )
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help='This field cannot be blank'
    )

    def post(self):
        data = self.parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {'message': 'User with that username already exists'}, 409

        user = UserModel(**data)
        user.save_to_db()

        return {'message': 'User created'}, 201


class User(Resource):

    @jwt_required()
    def delete(self, username):
        user = UserModel.find_by_username(username)
        if user:
            user.delete_from_db()
            return {'message': 'User deleted'}, 200

        return {'message': 'User not found'}, 404
