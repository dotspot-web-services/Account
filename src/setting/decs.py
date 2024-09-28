"""Perform operations as function or method decorator"""

import asyncio
import bz2
import datetime
import json
from functools import partial, update_wrapper
from typing import Any, Callable

import jwt
from cryptography.fernet import Fernet
from flask import request, session

from .dbcon import DbSet


class Auths:
    """decode auth and check validity"""

    def __init__(self, func: Callable[[int | str | None], Any] | str) -> None:
        self.__func = func
        self.db = DbSet()
        self._extusr: str = ""

    @property
    def _func(
        self,
    ) -> Callable[[int | str | None], Any] | str:
        """Set the function property

        Raises:
            Exception:  Raise an exception if self.func is not a function

        Returns:
            self.func:  return self.func if the instance is a function
        """
        return self.__func

    @_func.setter
    def _func(self, value: Callable[[int | str | None], Any] | str) -> None:
        if not (isinstance(value, str) or callable(value)):
            raise ValueError("value error")
        if callable(value):
            update_wrapper(self, value)
        self.__func = value

    def useracts(self) -> None:
        """user users ip or tpken to cache activities"""
        key: str = request.remote_addr

        if self._extusr:
            key = key + " " + self._extusr

    def encode_auth(self, **duration: float) -> bytes | str:
        """This generates an encoded auth for a user
        Args:
            status (bool, optional):  Defaults to True.
            duration (kwargs):  Timedelta key value pair argument as dict

        Returns:
            jwt.encode:  User generated Auth Token
        """

        try:
            payload: Any = {
                "iat": datetime.datetime.now(datetime.UTC),
                "usr": self.__func,
            }
            if duration:  # "=".join(key, val) for key, val in duration.items()
                duratn = datetime.timedelta(**duration)
                payload["exp"] = datetime.datetime.now(datetime.UTC) + duratn
            return jwt.encode(
                payload=payload, key=self.db._oda.secret, algorithm="HS256"
            )
        except jwt.PyJWKSetError as err:
            return f"Invalid token encoding{err}"

    async def get_auth(self, data: dict[str, str]) -> int | None:
        """asynchronous method of accessing token"""

        async with self.db.get_db() as conn:
            async with self.db._model.get_usr(conn, usr=data["usr"]) as cur:
                usr: int = cur.fetchone()
                return usr
        await asyncio.run(self.get_auth(data=data))

    def authenticate(self) -> int | str:
        """Authenticate and return a user

        Returns:
            user(int), exp(date), timed(Bool):  user id,
            the expiration time and token status
        """

        if not (
            token := session.get("token") or request.headers.get("authorization", "")
        ):
            return "Token is missing"

        if not session:
            token = token.split(" ")[1]
        try:
            data = jwt.decode(token, self.db._oda.secret, algorithms=["HS256"])
            extusr = data["usr"]
            usr = self.db._model.get_usr(self.db.get_db(data_level=2), usr=extusr)
            self._cache = extusr
        except jwt.ExpiredSignatureError:
            return "Expired token"
        # except jwt.DecodeError as err:
        #     return 401, f"Invalid token {err}"
        # now = datetime.datetime.now()
        # if (exp :=  data.get('exp', None)) and exp < now:
        #     return usr, True
        return usr

    def __call__(
        self, instance: int | str
    ) -> Callable[[int | str | None], Any] | dict[str, Any]:
        if not isinstance(self.__func, str):
            auth = self.authenticate()
            return self.__func(auth)
        else:
            raise Exception("not a function")


class Auth(Auths):
    def __get__(
        self,
        instance: int | str,
        owner: int,
    ) -> Any:
        return partial(self, instance)

    def __call__(self, instance: int | str) -> Callable[[int | str | None], Any]:
        if not isinstance(self.__func, str):
            # auth = self.authenticate()
            return self.__func(instance)
        else:
            raise Exception("not a function")
        # if len(auth) == 2:
        #     usr, status = self.authenticate()
        #     return self.func(instance, usr)
        # elif len(auth) == 1:
        #     usr = self.authenticate()


class Cache(Auths):
    def __init__(
        self,
        func: Callable[[int | str | None], Any] | str = "",
    ) -> None:
        super().__init__(func)
        self.__cache = self.db.get_redis(db=10)
        self.__cipher = Fernet(Fernet.generate_key())

    def compencrpt(self, data: dict[str, Any]) -> bytes:
        data_encrypt = self.__cipher.encrypt(json.dumps(data).encode("utf-8"))

        return bz2.compress(data_encrypt)

    def decompdecrypt(self, data: bytes) -> dict[str, Any]:
        decompressed_data = bz2.decompress(data=data)
        encrypted_data = self.__cipher.decrypt(decompressed_data)
        return json.loads(encrypted_data)

    def freqdata(self, key: str, data: dict[str, Any]) -> None:
        """cache according to top searches access using search string as key

        Args:
            key (str):  this is the key of the  cache and it expires
            data (json):  json data from the api
        """

        if key := request.values:
            encrypt_data = self.compencrpt(data=data)
            self.__cache.set(name=key, value=encrypt_data, ex=600, nx=True)

    def topdata(self, key: str, data: dict[str, str]) -> None:
        # note geolocation of data access using ip address
        """cache according to top searches access using search string as key

        Args:
            key (str):  this is the key of the  cache and it expires
            data (json):  json data from the api
        """

        if key := request.values:
            encrypt_data = self.compencrpt(data=data)
            self.__cache.set(name=key, value=encrypt_data, ex=600, nx=True)

    def quemsg(self, user_data: dict[str, str], queue_name: str) -> None:
        """push tasks into redis que for processing"""

        db = DbSet().get_redis(db=1)
        encrypt_data = self.compencrpt(data=user_data)
        db.lpush(queue_name, encrypt_data)

    def __get__(self, instance: int | str, owner: int) -> Any:
        return partial(self, instance)

    def __call__(
        self,
        instance: int | str,
    ) -> Callable[[int | str | None], Any] | dict[str, Any]:
        """cache with either user ip or user external id
        more than one account can logged in a single device
        """

        key: str = request.values
        if from_cache := self.__cache.get(key):
            return self.decompdecrypt(data=from_cache)
        else:
            if not isinstance(self.__func, str):
                data = self.__func(instance)
                self.freqdata(key=key, data=data)
            return data


class Responder:
    """manage request response operations"""

    def __init__(
        self,
        func: Callable[
            [int | str | None],
            tuple[dict[str, Any], int] | int,
        ],
    ) -> None:
        """decorator for examining and returning appropriate response

        Args:
            status_code (int):  http status response code
            data (dict or string, optional): dict for data; string for error.
            Defaults to None.
        """

        self._func = func
        self.status: int = 0
        self.data: dict[str, Any] | str | int = {}

    @property
    def func(
        self,
    ) -> Callable[
        [int | str | None],
        tuple[dict[str, Any], int] | int,
    ]:
        """variable _func setter"""
        return self._func

    @func.setter
    def func(
        self,
        value: Callable[
            [int | str | None],
            tuple[dict[str, Any], int] | int,
        ],
    ) -> None:
        if not callable(value):
            raise ValueError(f"error: {type(value)} cannot be decorated")
        self._func = value
        update_wrapper(self, value)

    def respons(self) -> dict[str, str]:
        """return an http response code determined message

        Returns:
            dict:  dictionary response message
        """
        msg: dict[str, str] = {"message": "operation is successful"}

        if self.status == 200 or self.status == 201:
            return msg
        elif self.status == 401:
            msg["message"] = "Unauthorized operation"
        elif self.status == 409:
            msg["message"] = "Duplicate data operation"
        elif self.status == 422:
            msg["mesage"] = "Invalid data operation"
        return msg

    def __call__(self, instance: int | str | None) -> tuple[dict[str, Any], int]:
        func = self._func(instance)

        if isinstance(func, tuple):
            self.data, self.status = func
        else:
            self.status = func
            self.data = self.respons()
        return self.data, self.status


class Responders(Responder):
    """Response operations in decorator"""

    def __get__(
        self,
        instance: Callable[..., tuple[dict[str, Any], int]],
        owner: int,
    ) -> partial[tuple[dict[str, Any], int]]:
        return partial(self, instance)

    def __call__(self, instance: int | str | None) -> tuple[dict[str, Any], int]:
        func = self._func(instance)

        if isinstance(func, tuple):
            self.data, self.status = func
        else:
            self.status = func
            self.data = self.respons()
        return self.data, self.status
