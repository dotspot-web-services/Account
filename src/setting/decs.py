
import asyncio
import datetime
from functools import update_wrapper, partial

import jwt
from flask import request, make_response
from pydantic.types import UUID1

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

    def encode_auth(self, status=True, **duration):
        """
        Generates the Auth Token
        :return: string
        """
        duratn = datetime.timedelta("=".join(key, val) for key, val in duration.items())
        
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + duratn,
                'iat': datetime.datetime.utcnow(),
                'usr': self.func,
                'status': status,
            }
            return jwt.encode(payload, self.db._oda.secret, algorithm='HS256')
        except Exception:
            return 401, "Invalid token"

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
            return 401, "Token is missing"
        try:
            data = jwt.decode(token, self.db._oda.secret, algorithms=["HS256"])
            usr = self.db._model.get_usr(self.db.get_db(data_level=2), usr=data['usr'])
        except jwt.ExpiredSignatureError or jwt.DecodeError:
            return 401, "invalid or an expired token"
        return usr, data['exp'], data['timed']

    def __call__(self):
        (auth := self.authenticate())
        if len(auth) == 2:
            usr, status = self.authenticate()
            return self.func(usr, status)
        elif len(auth) == 3:
            usr, status, timed_token = self.authenticate()
        if timed_token is True:
            return self.func(usr, status)
        return self.func(usr.usr)

class Auth(Auths):

    def __get__(self, instance, owner):
        return partial(self, instance)

    def __call__(self, instance):

        (auth := self.authenticate())

        if len(auth) == 2:
            usr, status = self.authenticate()
            return self.func(instance, usr, status)
        elif len(auth) == 3:
            usr, status, timed_token = self.authenticate()
        if timed_token is True:
            return self.func(instance, usr, status)
        return self.func(instance, usr.usr, None)

class Responder(object):

    def __init__(self, func) -> None:
        """decorator for examining and returning appropriate response

        Args:
            status_code (int): http status response code
            data (dict or string, optional): dict if data is feched but string when reporting an error. Defaults to None.
        """
        update_wrapper(self, func)
        self.func = func
        self.status = None
        self.data = None
        
        if not callable(self.func):
            raise Exception(f"error:{type(self.func)} cannot be decorated")
        

    def message(self):
        """return an http response code determined message

        Returns:
            dict: dictionary response message
        """
        msg = {"message": "operation is successful"}
        
        if self.status > 199 <= 203 and isinstance(self.data, (dict, list, str)):
            msg = self.data
        elif self.status > 199 <= 203 :
            pass
        elif self.status > 399 <= 403 and self.data is None:
            msg["message"] = "invalid data submision"
        elif self.status == 404:
            msg["message"] = "Item is not found in resource"
        elif self.status > 399 <= 403 and self.data is not None:
            msg["message"] = self.data
        return msg

    def response(self):
        """return an http response code and data or message as determined data

        Returns:
            dict: dictionary response message or data
        """
        if msg := self.message():
            return self.status, msg

    def __call__(self):

        (func := self.func())

        if isinstance(func, tuple):
            self.status, self.data = func
        else:
            self.status = func
        if resp := self.response():
            status, data = resp
        return data, status
        

class Responders(Responder):

    def __get__(self, instance, owner):
        return partial(self, instance)

    def __call__(self, instance):

        (func := self.func(instance))
        if isinstance(func, tuple):
            self.status, self.data = func
        else:
            self.status = func
        if resp := self.response():
            status, data = resp
        return data, status


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
