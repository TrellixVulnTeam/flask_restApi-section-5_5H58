
from flask_restful import Resource, reqparse
from models.user import UserModel 
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from passlib.hash import pbkdf2_sha256






# class UserRegister(Resource):
#     parser = reqparse.RequestParser()
#     parser.add_argument('username',
#                         type=str,
#                         required=True,
#                         help="This field cannot be blank."
#                         )
#     parser.add_argument('password',
#                         type=str,
#                         required=True,
#                         help="This field cannot be blank."
#                         )

#     def post(self):
#         data = UserRegister.parser.parse_args()

#         if UserModel.find_by_username(data['username']):
#             return {"message": "A user with that username already exists"}, 400

#         user = UserModel(data['username'], data['password'])
#         user.save_to_db()

#         return {"message": "User created successfully."}, 201




class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    def post(self):
        data = UserRegister.parser.parse_args()
        
        if UserModel.find_by_username(data['username']):
            return {'message': 'User {} already exists'.format(data['username'])}
        
        new_user = UserModel(
            username = data['username'],
            password = UserModel.generate_hash(data['password'])
        )
        
        try:
            new_user.save_to_db()
            access_token = create_access_token(identity = data['username'])
            
            return {
                'message': 'User {} was created'.format(data['username']),
                'access_token': access_token
                }
        except:
            return {'message': 'Something went wrong'}, 500



class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    
    def post(self):
        data = UserRegister.parser.parse_args()
        current_user = UserModel.find_by_username(data['username'])

        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(data['username'])}
        
        if UserModel.verify_hash(data['password'], current_user.password):
            access_token = create_access_token(identity = data['username'])
            return {
                'message': 'Logged in as {}'.format(current_user.username),
                'access_token': access_token
                }
        else:
            return {'message': 'Wrong credentials'}