
import asyncio
import datetime
import time
from functools import update_wrapper, partial
from typing import Callable
import ipaddress
import json
import bz2


import jwt
from flask import request, make_response, session
from cryptography.fernet import Fernet

from .dbcon import DbSet

class Auths(object):
    """decode auth and check validity"""

    def __init__(self, func:Callable|str):
        
        self._func = func
        update_wrapper(self, self._func)
        self.db = DbSet()
        self._extusr = ""

    @property
    def _func(self):
        """ Set the function property

        Raises:
            Exception: Raise an exception if self.func is not a function 

        Returns:
            self.func: return self.func if the instance is a function
        """
        return self.__func
    
    @_func.setter
    def _func(self, value:Callable|str):
        if not isinstance(value, (Callable, str)):
            raise Exception('value error')
        self.__func = value
        
    def useracts(self):
        """user users ip or tpken to cache activities
        """
        key = request.remote_addr
        
        if self._extusr:
            key = key + " " + self._extusr 
        pass
    
    def encode_auth(self, **duration):
        """This generates an encoded auth for a user
        Args:
            status (bool, optional): Defaults to True.
            duration (kwargs): Timedelta key value pair argument as dict

        Returns:
            jwt.encode: User generated Auth Token
        """
        
        try:
            payload = {
                'iat': datetime.datetime.utcnow(),
                'usr': self._func
            }
            if duration:#"=".join(key, val) for key, val in duration.items()
                duratn = datetime.timedelta(**duration)
                payload['exp'] = datetime.datetime.utcnow() + duratn
            return jwt.encode(payload=payload, key=self.db._oda.secret, algorithm='HS256')
        except Exception as err:
            return 401, f"Invalid token encoding{err}" 

    async def get_auth(self, data):
        async with self.db.get_db() as conn:
            async with self.db._model.get_usr(conn, usr=data['usr']) as cur:
                print(cur.fetchone())
                self.usr = cur.fetchone()
        await asyncio.run(self.get_auth(data=data))

    def authenticate(self):
        """Authenticate and return a user 

        Returns:
            user(int), exp(date), timed(Bool): Authenticated user along the experation time and token time status 
        """

        if not (token := session.get("token") or  request.headers.get('authorization', "")) :
            return 401, "Token is missing"
        #print(f"no split: {self.}")no split: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2ODgzODE4NzcsInVzciI6ImFhYjZlMzJmLWYyOWEtNDMwZC1iYzYyLWYxZWQyNjAzODgwNCIsImV4cCI6MTY4ODY0MTA3N30.4D2dv_jwl0QokB6WrX2vlaJ07i6exlUkEpfQ8EaWX2w
        
        if not session: 
            token = token.split(" ")[1]
        #tkn = token.split(" ")splited not indexed: ['eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2ODgzODE4NzcsInVzciI6ImFhYjZlMzJmLWYyOWEtNDMwZC1iYzYyLWYxZWQyNjAzODgwNCIsImV4cCI6MTY4ODY0MTA3N30.4D2dv_jwl0QokB6WrX2vlaJ07i6exlUkEpfQ8EaWX2w']
        #print(f"splited: {tkn}")eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2ODgzODE4NzcsInVzciI6ImFhYjZlMzJmLWYyOWEtNDMwZC1iYzYyLWYxZWQyNjAzODgwNCIsImV4cCI6MTY4ODY0MTA3N30.4D2dv_jwl0QokB6WrX2vlaJ07i6exlUkEpfQ8EaWX2w
        try:
            data = jwt.decode(token, self.db._oda.secret, algorithms=["HS256"])
            extusr = data['usr']
            usr = self.db._model.get_usr(self.db.get_db(data_level=2), usr=extusr)
            self._cache = extusr
        except jwt.ExpiredSignatureError:
            return 401, "Expired token"
        #except jwt.DecodeError as err:
        #    return 401, f"Invalid token {err}"
        #now = datetime.datetime.now()
        #if (exp := data.get('exp', None)) and exp < now:
        #    return usr, True
        return usr

    def __call__(self):
        auth = self.authenticate()
        return self._func(auth)

class Auth(Auths):
    
    # RateLimitUsingTokenBucket .
    def RateLimitUsingTokenBucket(self, userID: str, intervalInSeconds: int, maximumRequests: int):
        addr = request.remote_addr
        reds = self.db.get_redis(8)
       #userID can be apikey, location, ip
        value, _ = reds.get(userID+"_last_reset_time")
        lastResetTime, _ = int(value, 10, 64)
       #if the key is not available, i.e., this is the first request, l astResetTime will be set to 0 and counter be set to max requests allowed
       #check if time window since last counter reset has elapsed
        if time.localtime()-lastResetTime >= intervalInSeconds:
           #if elapsed, reset the counter
            reds.set(userID+"_counter", int(maximumRequests, 10), 0)
        else:
            value, _ = reds.get(userID+"_counter")
            requestLeft, _ = int(value, 10, 64)
            if requestLeft <= 0: #request left is 0 or < 0
               #drop request
                return False
       #decrement request count by 1
        reds.decr(userID+"_counter")
        # handle request
        return True

    def ratelimit(self):

        # Where we put all the bad egg IP addresses
        blacklist = set()
        MAXVISITS = 15

        ipwatcher = self.db.get_redis(8)

        while True:
            _, addr = ipwatcher.blpop("ips")
            addr = ipaddress.ip_address(addr.decode("utf-8"))
            now = datetime.datetime.utcnow()
            addrts = f"{addr}:{now.minute}"
            n = ipwatcher.incrby(addrts, 1)
            if n >= MAXVISITS:
                print(f"Hat bot detected!:  {addr}")
                blacklist.add(addr)
            else:
                print(f"{now}:  saw {addr}")
            _ = ipwatcher.expire(addrts, 60)
            return
        
    def compres(self, rds, key, data):

        # Set the compressed string as value
        rds.set(key, bz2.compress(data.encode("utf-8")))

    def __get__(self, instance:object, owner:id):
        return partial(self, instance)

    def __call__(self, instance):

        auth = self.authenticate()
        return self._func(instance, auth)
        #if len(auth) == 2:
        #    usr, status = self.authenticate()
        #    return self.func(instance, usr)
        #elif len(auth) == 1:
        #    usr = self.authenticate()
        

class Cache(Auths):
    
    def __init__(self, func: Callable):
        super().__init__(func)
        self.__cache = self.db.get_redis(db=10)
    
    def compencrpt(self, data):
        
        cipher = Fernet(Fernet.generate_key())
        data_encrypt = cipher.encrypt(json.dumps(data).encode("utf-8"))
        
        return bz2.compress(data_encrypt.encode("utf-8"))
    
    def freqdata(self, key:str, data:json):
        """cache according to top searches access using search string as key

        Args:
            key (str): this is the key of the  cache and it expires
            data (json): json data from the api
        """
        
        if key := request.values:  
            self.compencrpt(data=data)
            self.__cache.set(name=key, value=data, ex=600, nx=True)
    
    def topdata(self, key:str, data:json):#take note of geolocation of access point using ip address
        """cache according to top searches access using search string as key

        Args:
            key (str): this is the key of the  cache and it expires
            data (json): json data from the api
        """
        
        if key := request.values:  
            self.compencrpt(data=data)
            self.__cache.set(name=key, value=data, ex=600, nx=True)
    
    def __get__(self, instance:object, owner:id):
        return partial(self, instance)

    def __call__(self, instance):
        """cache with either user ip or user external id in such a way more than one 
        account can logged in a single device
        """
        
        key = request.values
        if from_cache := self.__cache.get(key):
            return from_cache
        else:
            data = self._func(instance)
            return self.freqdata(key=key, data=data)
    

class Responder(object):

    def __init__(self, func:str) -> None:
        """decorator for examining and returning appropriate response

        Args:
            status_code (int): http status response code
            data (dict or string, optional): dict if data is feched but string when reporting an error. Defaults to None.
        """
        
        self._func = func
        update_wrapper(self, self._func)
        self.status:int = 0
        self.data:dict = {}
        
    @property
    def func(self):
        return self._func
    
    @func.setter
    def func(self, value):
        if not callable(value):
            raise Exception(f"error:{type(value)} cannot be decorated")
        self._func = value

    def respons(self):
        """return an http response code determined message

        Returns:
            dict: dictionary response message
        """
        msg = {"message": "operation is successful"}
        
        #if self.status > 199 <= 203 and self.data and isinstance(self.data, (dict, tuple, list, str)):
        #    msg = self.data
        if self.status == 200:
            return
        elif self.status == 201:
            return msg
        elif self.status == 401:
            msg["message"] = "Unauthorized operation"
            return msg
        elif self.status == 409:
            msg["message"] = "Duplicate data operation"
            return msg
        elif self.status == 422:
            return


class Responders(Responder):

    def __get__(self, instance:object, owner:id):
        return partial(self, instance)

    def __call__(self, instance):

        func = self._func(instance)
        if isinstance(func, tuple):
            self.status, self.data = func
        else:
            self.status = func
        if resp := self.respons():
            self.data = resp
        print(self.respons())
        return self.data, self.status


class Cors(object):

    def __init__(self, func:str=""):
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

    def __get__(self, instance:object, owner:id):
        return partial(self, instance)

    def __call__(self, instance):
        resp = self.func(instance)
        return self.corsify(resp=resp)
