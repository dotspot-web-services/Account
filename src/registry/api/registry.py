"""Handle registeration requests"""

import bcrypt
from bleach import clean
from flask import request
from flask_restful import Resource
from pydantic import ValidationError

from setting.dbcon import DbSet as _DBSET
from setting.decs import Auth as authenticate, Cache
from setting.decs import Responders as response
from setting.helper import convert_errors

from ..serializer import LogCheck, PwdCheck, RegCheck, finalCheck


class Register(Resource):
    """
    User Registration Resource
    """

    def __init__(self) -> None:
        self._db = _DBSET()
        self.cache = Cache()

    def __hash_pwd(self, pwd: str) -> bcrypt.hashpw:
        """User password encryption

        Args:
            pwd (str): User's provided password

        Returns:
            str: Hashed password
        """
        return bcrypt.hashpw(
            bytes(pwd, encoding="utf-8"), bcrypt.gensalt(self._db._oda.log_rod)
        )

    @response
    def post(self) -> tuple[int, dict[str, str] | str]:
        """A new user registeration

        Returns:
           status(int): The status of the registeration request sent
        """

        reg_data = request.form or request.get_json()
        code: int = 422
        data: str | dict[str, str] = ""

        try:
            check = RegCheck(
                fname=reg_data.get("fname"),
                cont=reg_data.get("cont"),
                pwd=reg_data.get("pwd"),
                vpwd=reg_data.get("vpwd"),
            )
        except ValidationError as err:
            errors = convert_errors(err=err)
            data = errors
        # if check.cnt == check.EmailStr:
        #    cntyp = False
        #    print(check.EmailStr)
        # elif check.cnt == check.phone:
        #    cntyp = True
        #    print(check.phone)

        with self._db.get_db(data_level=2) as con:
            if self._db._model.check_acc(con, contact=check.cont):
                code = 409
            if usr := self._db._model.cr8_acc(
                con,
                fname=clean(check.fullname),
                pwd=self.__hash_pwd(pwd=check.pwd).decode("utf8"),
                cnt=check.cnt,
            ):
                self.cache.quemsg(
                    user_data=check.model_dump(exclude={"pwd", "pwd2"}),
                    queue_name="newAccount",
                )
                token = authenticate(func=usr).encode_auth(days=1)
                code = 201
                data = token
        return code, data

    @response
    @authenticate
    def put(self, usr: int | str) -> tuple[int, dict[str, str] | str]:
        """Complete preprofile data

        Args:
            usr (int): the user from token authentication
            token_status (Bool): The status of the token, if it can expire

        Returns:
            response_code(int): The status code of the response
            response_message(str): The response status message
        """

        code: int = 422
        data: str | dict[str, str] = ""

        if isinstance(usr, str):
            return 401, usr

        reg_data = request.get_json()

        try:
            check = finalCheck(
                fname=reg_data.get("fname"),
                cont=reg_data.get("cont"),
                dob=reg_data.get("dob"),
                cntyp=reg_data.get("typ"),
                sx=reg_data.get("sx"),
            )
        except ValidationError as err:
            data = convert_errors(err=err)
            return code, data

        with self._db.get_db() as con:
            code = 200
            if self._db._model.upd8_acc(
                con,
                usr=usr,
                fname=clean(check.fullname),
                cnt=check.cnt,
                emel=check.cntyp,
                bday=check.dob,
                mel=check.sex,
                actv=True,
                verfd=True,
            ):
                self.cache.quemsg(
                    user_data=check.model_dump(exclude={"cont", "dob", "cntyp", "sx"}),
                    queue_name="createArena",
                )
                code = 401
        return code, data

    @response
    def get(self) -> tuple[int, dict[str, str] | str]:
        """Fetch users registeration data

        Returns:
            response_code(int): The status code of the response
            response_message(str): The response status message
        """

        code: int = 404
        data: str | dict[str, str] = ""
        qs = request.values
        contact = qs["contact"]

        with self._db.get_db() as con:
            if cont := self._db._model.get_cont(con, cnt=contact):
                code = 201
                data = cont
        return code, data

    def options(self) -> tuple[dict[str, list[str]], int, dict[str, str]]:
        """For handling core operations"""

        return (
            {"Allow": ["POST", "GET"]},
            200,
            {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "*",
                "Access-Control-Allow-Headers": "*",
                "cross-site-cookies": "session",
                "samesite": "Lax",
            },
        )


class Login(Register):
    """
    User Login Resource
    """

    @response
    def post(self) -> tuple[int, dict[str, str] | str] | int:
        """
        Check user account status
        Check password
        Generate a token

        Returns:
            response_code(int): The status code of the response
            response_message or token(str): status message or user token
        """
        # get the post data

        code: int = 422
        data: str | dict[str, str] = ""

        if not (auth := request.authorization or request.form):
            return 401
        (contact := auth.get("cont") or auth.username)
        (password := auth.get("pwd") or auth.password)

        try:
            check = LogCheck(cont=contact, pwd=password)
        except ValidationError as err:
            data = convert_errors(err=err)
            return code, data

        with self._db.get_db(data_level=2) as con:
            if (
                (usr := self._db._model.check_acc(con, contact=check.cont))
                and usr is None
                or not usr
            ):
                code = 404
            if bcrypt.checkpw(
                password=check.pwd.encode("utf-8"),
                hashed_password=usr.pwd.encode("utf-8"),
            ):
                if (
                    usr_data := self._db._model.usr_status(con, contact=check.cont)
                ) and usr_data.token == "":
                    token = authenticate(func=usr.usr).encode_auth(days=3)
                    self._db._model.cr8_tkn(con, tkn=token)
                    # notification Email for new device login
                    # self.cache.quemsg(user_data=check, queue_name="account changes")
                    code = 200
                    data = {"token": str(token)}
                if usr_data.user_status is False:
                    code = 401
                    data = "Account is not activated yet"
                code = 201
                data = usr_data.token
        return code, data

    @response
    @authenticate
    def put(self, usr: int | str) -> tuple[int, dict[str, str] | str]:
        """
        Check if the account request token is expired
        Udate the password and login the person
        Args:
            usr (int): the user from token authentication
            token_status (Bool): The status of the token, if it is time bound

        Returns:
            response_code(int): The status code of the response
            response_message(str): The response status message
        """

        # if token_status:
        #    redirect(url_for('accs.regs.finalize'))
        code: int = 422
        data: str | dict[str, str] = ""

        if isinstance(usr, str):
            return 401, usr

        reg_data = request.get_json()

        try:
            check = PwdCheck(
                cont=reg_data.get("cont"),
                pwd=reg_data.get("pwd"),
                vpwd=reg_data.get("vpwd"),
            )
        except ValidationError as err:
            data = convert_errors(err=err)
            return code, data

        with self._db.get_db() as con:
            code = 201
            if self._db._model.upd8_pwd(
                con, usr=usr, pwd=self.__hash_pwd(pwd=check.pwd).decode("utf8")
            ):
                self.cache.quemsg(
                    user_data=check.model_dump(exclude={"pwd", "vpwd"}),
                    queue_name="accountChanges",
                )
                code = 401
        return code, data

    @response
    def get(self) -> tuple[int, dict[str, str] | str]:
        """Check if a user already exists through the contact

        Returns:
            response_code(int): The status code of the response
            response_message(str): The response status message
        """

        contact = request.form["cont"]
        code: int = 401
        data: str | dict[str, str] = ""

        with self._db.get_db() as con:
            if cont := self._db._model.get_cont(con, cnt=contact):
                code = 200
                data = cont
        return code, data


class Logout(Resource):
    """
    Logout Resource
    """

    def __init__(self) -> None:
        self._db = _DBSET()

    @response
    @authenticate
    def post(self, usr: int | str) -> tuple[int, dict[str, str] | str] | int:
        """
        Blacklist token

        Args:
            usr (_type_): _description_
            token_status (_type_): _description_

        Returns:
            _type_: _description_
        """
        # get auth token
        # if isinstance(usr, Tuple) and usr.usr != 401:
        #    usr = usr.usr

        auth_header = request.headers.get("Authorization")
        code: int = 401
        data: str | dict[str, str] = ""

        if not auth_header:
            code = 403
            return code

        auth_token = auth_header.split(" ")[1]

        if auth_token:
            code = 401
            if authenticate(func=auth_token).decode_auth():
                with self._db.get_db() as con:
                    self._db._model.in_tkn(con, tkn=auth_token, usr=usr)
                    code = 201
        return code, data

    @response
    def get(self, usr: int | str) -> tuple[int, dict[str, str] | str]:
        """Refresh access token if expired

        Args:
            usr (_type_): _description_

        Returns:
            _type_: _description_
        """
        code: int = 401
        data: str | dict[str, str] = ""

        with self._db.get_db(data_level=1) as con:
            if data := self._db._model.usr_reg(con, usr=usr):
                code = 200
        return code, data

    def options(self) -> tuple[dict[str, list[str]], int, dict[str, str]]:
        """Core settings operations"""

        return (
            {"Allow": ["POST", "GET"]},
            200,
            {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "*",
                "Access-Control-Allow-Headers": "*",
                "cross-site-cookies": "session",
                "samesite": "Lax",
            },
        )


class Reset(Logout):
    """
    Logout Resource
    """

    @response
    def post(self) -> tuple[int, dict[str, str] | str]:
        """Check if a user already exists through the contact

        Returns:
            response_code(int): The status code of the response
            response_message(str): The response status message
        """

        contact = request.form["cont"]
        code: int = 401
        data: str | dict[str, str] = ""

        with self._db.get_db() as con:
            if cont := self._db._model.get_cont(con, cnt=contact):
                self.cache.quemsg(user_data={"cont": cont}, queue_name="resetAccount")
                code = 201
        return code, data

    @response
    def get(self, usr: int | str) -> tuple[int, dict[str, str] | str]:
        """Refresh access token if expired

        Args:
            usr (_type_): _description_

        Returns:
            _type_: _description_
        """
        code: int = 401
        data: str | dict[str, str] = ""

        with self._db.get_db(data_level=1) as con:
            if data := self._db._model.usr_reg(con, usr=usr):
                code = 200
        return code, data
