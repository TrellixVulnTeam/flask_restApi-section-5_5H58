import os
import sqlite3
from datetime import datetime
from functools import wraps

import jwt
from flask import Flask, request, abort, g

from .utils import json_response, error_response
from models.user import UserModel

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', '$SECRET$')



class UserLogin(Resource):
    data = UserModel.request.get()

    if not all(['username' in data, 'password' in data]):
        return error_response('Missing username or password')
    username, password = [data[f] for f in ('username', 'password')]
    user = authenticate_user(username, password)
    if not user:
        return error_response('Invalid Credentials')

    token = jwt.encode({'username': username}, app.config['SECRET_KEY'])

    return json_response({'token': token.decode('utf-8')})