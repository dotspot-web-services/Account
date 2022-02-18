
import asyncio
import datetime
from functools import update_wrapper, partial

import jwt
from flask import jsonify, redirect, request, make_response
from pydantic.types import UUID1
from werkzeug import Response

from .dbcon import DbSet

class Auths(object):
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

    def encode_auth(self,  status=True):
        """
        Generates the Auth Token
        :return: string
        """
        if status:
            duratn = datetime.timedelta(days=3.0)
            token_status = True
        else:
            duratn = datetime.timedelta()
            token_status = False
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + duratn,
                'iat': datetime.datetime.utcnow(),
                'usr': self.func,
                'status': status,
                'timed': token_status
            }
            return jwt.encode(payload, self.db._oda.secret, algorithm='HS256')
        except Exception as e:
            return e

    async def get_auth(self, data):
        async with self.db.get_db() as conn:
            async with self.db._model.get_usr(conn, usr=data['usr']) as cur:
                print(cur.fetchone())
                self.usr = cur.fetchone()
        await asyncio.run(self.get_auth(data=data))

    def authenticate(self):

        token = None
        token = request.headers.get('authorization') 

        if token is None:
            return jsonify({"message": "Token is missing"})
        try:
            data = jwt.decode(token, self.db._oda.secret, algorithms=["HS256"])
            usr = self.db._model.get_usr(self.db.get_db(data_level=2), usr=data['usr'])
        except jwt.ExpiredSignatureError or jwt.DecodeError:
            return redirect(self.db._oda.dormain)
        return usr, data['exp'], data['timed']

    def __call__(self):
        
        if (auth := isinstance(self.authenticate(), Response)):
            return auth
        usr, status, timed_token = self.authenticate()
        if timed_token is True:
            return self.func(usr, status)
        return self.func(usr.usr)

class Auth(Auths):

    def __get__(self, instance, owner):
        return partial(self, instance)

    def __call__(self, instance):
        if (auth := self.authenticate()) and isinstance(auth, Response):
            return auth
        usr, status, timed_token = self.authenticate()
        if timed_token is True:
            return self.func(instance, usr, status)
        return self.func(instance, usr.usr, None)


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

    def _build_cors_prelight_response(self, resp_obj):
        #resp = current_app.make_default_options_response()
        resp = make_response(resp_obj)
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
            core = self._build_cors_prelight_response(resp_obj=resp)
        else:
            core = self._build_cors_prelight_response(resp_obj=resp)
        return core

    def __get__(self, instance, owner):
        return partial(self, instance)

    def __call__(self, instance):
        resp = self.func(instance)
        return self.corsify(resp=resp)
