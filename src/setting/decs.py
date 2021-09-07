
import datetime
from functools import update_wrapper, partial

import jwt
from flask import jsonify, request, make_response
from pydantic.types import UUID1

from .dbcon import DbSet

class Auth(object):
    """decode auth and check validity"""

    def __init__(self, func):
        update_wrapper(self, func)
        self.func = func
        self.db = DbSet()

    @property
    def action(self):
        if isinstance(self.func, (function, UUID1)):
            return self.func
        raise Exception('value error')

    def encode_auth(self):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=100),
                'iat': datetime.datetime.utcnow(),
                'usr': self.func
            }
            return jwt.encode(payload, self.db._oda.secret, algorithm='HS256')
        except Exception as e:
            return e

    
    def authenticate(self):
        token = None
        token = request.headers.get('authorization', None)
        
        if token is None:
            return jsonify({'message': 'Token is missing'})
        try:
            data = jwt.decode(token, self.db._oda.secret, algorithms=["HS256"])
            usr = self.db._model.get_usr(self.db.get_db(dict=True), usr=data['usr'])
        except jwt.ExpiredSignatureError as err:
            return jsonify({'message': f'Token is invalid {err}'}), 401
        return usr

    def __get__(self, instance, owner):
        return partial(self, instance)

    def __call__(self, instance):
        return self.func(instance, self.authenticate())

class Cors(object):

    def __init__(self, func=None):
        update_wrapper(self, func)
        self.func = func

    def decorator(number):
        def inner(f):
            def decorator_f(*args, **kwargs):
                result = f(*args, **kwargs)
                #make some manipulation on result
                return result
            return decorator_f
        return inner

    def _build_cors_prelight_response(self, resp):
        #resp = current_app.make_default_options_response()
        resp.headers.add("Access-Control-Allow-Origin", "*")
        resp.headers.add('Access-Control-Allow-Headers', "*")
        resp.headers.add('Access-Control-Allow-Methods', "*")
        return resp
    
    def _corsify_actual_response(self, resp_obj):
        resp = make_response(resp_obj)
        resp.headers.add("Access-Control-Allow-Origin", "*")
        return resp

    def corsify(self, resp):

        if request.method == "POST":
            core = self._corsify_actual_response(resp_obj=resp)
        elif request.method == "OPTIONS":
            core = self._build_cors_prelight_response(resp=resp)
        else:
            core = self._build_cors_prelight_response(resp=resp)
        return core

    def __get__(self, instance, owner):
       return partial(self, instance)

    def __call__(self, instance):
        resp = self.func(instance)
        return self.corsify(resp=resp)
