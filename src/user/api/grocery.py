"""user external activities resource"""

from bleach import clean
from flask import request
from flask_restful import Resource
from pydantic import ValidationError

from setting.dbcon import DbSet as _DBSET
from setting.decs import Auth as authenticate
from setting.decs import Responders as response
from setting.helper import convert_errors
from user.grocerySerializer import CreateAward, CreateSoc, Object


class Awards(Resource):
    """
    User Resource
    """

    def __init__(self) -> None:
        self._db = _DBSET(sql_filename="groce.pgsql")

    @response
    @authenticate
    def post(self, usr: int | str) -> tuple[int, dict[str, str] | str]:
        """Register user's award profile as many as user have

        Args:
            usr (int): the user from token authentication
            token_status (Bool): The status of the token, if it is time bound

        Returns:
            response_code(int): The status code of the response
            response_message(str): The response status message
        """

        code: int = 422
        data: str | dict[str, str] = ""

        if isinstance(usr, str):
            return 401, usr

        try:
            awd_data = request.get_json()
            check = CreateAward(
                plc=awd_data.get("locatn"),
                act=awd_data.get("orgsatn"),
                ttl=awd_data.get("ttl"),
                awdt=awd_data.get("awdt"),
            )
        except ValidationError as err:
            data = convert_errors(err=err)
            return code, data

        with self._db.get_db() as con:
            self._db._model.cr8_awd(
                con,
                usr=usr,
                plc=clean(check.plc),
                acts=clean(check.acts),
                titl=clean(check.ttl),
                awdt=check.awdt,
            )
            code = 201
        return code, data

    @response
    @authenticate
    def get(self, usr: int | str) -> tuple[int, dict[str, str] | str]:
        """Fetct a record of user's work profile
        Args:
            usr (int): the user from token authentication
            token_status (Bool): The status of the token, if it is time bound

        Returns:
            response_code(int): The status code of the response
            response_message(str): The response status message
        """

        code: int = 404
        data: str | dict[str, str] = ""

        if isinstance(usr, str):
            return 401, usr

        if not (qs := request.values):
            usr_data = usr

        with self._db.get_db(data_level=1) as con:
            code = 201
            if usr_data:
                data = self._db._model.usr_awds(con, usr=usr)
            elif data_id := qs.get("id"):
                data = self._db._model.awd(con, data_id=data_id)
            elif srch := qs["srch"]:
                data = self._db._model.awds(con, usr=usr, pg=srch)
        return code, data

    @response
    @authenticate
    def put(self, usr: int | str) -> tuple[int, dict[str, str] | str]:
        """Update a record of user's work profile
        Args:
            usr (int): the user from token authentication
            token_status (Bool): The status of the token, if it is time bound

        Returns:
            response_code(int): The status code of the response
            response_message(str): The response status message
        """

        code: int = 422
        data: str | dict[str, str] = ""

        if isinstance(usr, str):
            return 401, usr

        try:
            awd_data = request.get_json()
            check = CreateAward(
                plc=awd_data.get("locatn"),
                act=awd_data.get("orgsatn"),
                ttl=awd_data.get("ttl"),
                awdt=awd_data.get("dt"),
                awd=awd_data.get("award"),
            )
        except ValidationError as err:
            data = convert_errors(err=err)
            return code, data

        with self._db.get_db() as con:
            code = 401
            if self._db._model.awd_rit(con, usr=usr, awd=check.obj):
                self._db._model.cr8_awd(
                    con,
                    usr=usr,
                    plc=clean(check.plc),
                    acts=clean(check.acts),
                    titl=clean(check.ttl),
                    awdt=check.awdt,
                )
                code = 201
        return code, data

    @response
    @authenticate
    def delete(self, usr: int | str) -> tuple[int, dict[str, str] | str]:
        """Delete a record of user's work profile

        Args:
            usr (int): the user from token authentication
            token_status (Bool): The status of the token, if it is time bound

        Returns:
            response_code(int): The status code of the response
            response_message(str): The response status message
        """

        code: int = 404
        data: str | dict[str, str] = ""

        if isinstance(usr, str):
            return 401, usr

        awd = request.values

        if not (check := Object(plc=awd.get("awd"))):
            return code, data
        with self._db.get_db() as con:
            code = 401
            if self._db._model.awd_rit(con, usr=usr, awd=check.obj):
                self._db._model.del_awd(con, usr=usr, awd=check.obj)
                code = 201
        return code, data

    def options(self) -> tuple[dict[str, list[str]], int, dict[str, str]]:
        """cross site permissions"""

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


class Socs(Awards):
    """API for all hubbies or interests outside studies"""

    @response
    @authenticate
    def post(self, usr: int | str) -> tuple[int, dict[str, str] | str] | int:
        """Register user's hubby profile
        Args:
            usr (int): the user from token authentication
            token_status (Bool): The status of the token, if it is time bound

        Returns:
            response_code(int): The status code of the response
            response_message(str): The response status message
        """

        code: int = 422
        data: str | dict[str, str] = ""

        if isinstance(usr, str):
            return 401, usr

        try:
            soc_data = request.get_json()
            check = CreateSoc(titl=soc_data.get("titl"), typ=soc_data.get("typ"))
        except ValidationError as err:
            data = convert_errors(err=err)
            return code, data

        with self._db.get_db() as con:
            self._db._model.cr8_soc(
                con, usr=usr, typ=clean(check.typ), ttl=clean(check.title)
            )
            code = 201
        return code

    @response
    @authenticate
    def get(self, usr: int | str) -> tuple[int, dict[str, str] | str] | int:
        """Fetch a user's hubby profile

        Args:
            usr (int): the user from token authentication
            token_status (Bool): The status of the token, if it is time bound

        Returns:
            response_code(int): The status code of the response
            response_message(str): The response status message
        """

        code: int = 401
        data: str | dict[str, str] = ""

        if isinstance(usr, str):
            return 401, usr

        if not (qs := request.values):
            usr_data = usr

        with self._db.get_db(data_level=1) as con:
            code = 201
            if usr_data:
                data = self._db._model.usr_socs(con, usr=usr)
            elif srch := qs["srch"]:
                data = self._db._model.socs(con, usr=usr, pg=srch)
            if id := qs.get("id"):  # takes user to social arena
                data = self._db._model.soc(con, usr=usr, id=id)
        return code, data

    @response
    @authenticate
    def put(self, usr: int | str) -> tuple[int, dict[str, str] | str] | int:
        """Update a user's hubby profile

        Args:
            usr (int): the user from token authentication
            token_status (Bool): The status of the token, if it is time bound

        Returns:
            response_code(int): The status code of the response
            response_message(str): The response status message
        """

        code: int = 422
        data: str | dict[str, str] = ""

        if isinstance(usr, str):
            return 401, usr

        try:
            soc_data = request.get_json()
            check = CreateSoc(titl=soc_data.get("ttl"), typ=soc_data.get("typ"))
        except ValidationError as err:
            data = convert_errors(err=err)
            return code, data

        with self._db.get_db() as con:
            code = 401
            if self._db._model.soc_rit(con, usr=usr, awd=check.obj):
                self._db._model.upd8_soc(
                    con, usr=usr, typ=clean(check.typ), ttl=clean(check.title)
                )
                code = 201
        return code

    @response
    @authenticate
    def delete(self, usr: int | str) -> tuple[int, dict[str, str] | str]:
        """Delete a user's hubby profile

        Args:
            usr (int): the user from token authentication
            token_status (Bool): The status of the token, if it is time bound

        Returns:
            response_code(int): The status code of the response
            response_message(str): The response status message
        """

        code: int = 422
        data: str | dict[str, str] = ""

        if isinstance(usr, str):
            return 401, usr

        soc = request.values

        if not (check := Object(obj=soc.get("soc"))):
            return code, data
        with self._db.get_db() as con:
            code = 401
            if self._db._model.soc_rit(con, usr=usr, soc=check.obj):
                self._db._model.del_soc(con, usr=usr, soc=check.obj)
                code = 201
        return code, data


class Avatars(Socs):
    """
    basic education or acquired skill
    """

    @response
    @authenticate
    def get(self, usr: int | str) -> tuple[int, dict[str, str] | str]:
        """Fetch a user's profile picture

        Args:
            usr (int): the user from token authentication
            token_status (Bool): The status of the token, if it is time bound

        Returns:
            response_code(int): The status code of the response
            response_message(str): The response status message
        """

        code: int = 404
        data: str | dict[str, str] = ""

        if isinstance(usr, str):
            return 401, usr

        if not (qs := request.values):
            usr_data = usr

        with self._db.get_db(data_level=1) as con:
            code = 201
            if usr_data:
                data = self._db._model.pix(con, usr=usr_data)
            elif id := qs.get("id"):
                data = self._db._model.pixs(con, usr=usr, id=id)
        return code, data

    @response
    @authenticate
    def delete(self, usr: int | str) -> tuple[int, dict[str, str] | str]:
        """Delete a user's profile picture

        Args:
            usr (int): the user from token authentication
            token_status (Bool): The status of the token, if it is time bound

        Returns:
            response_code(int): The status code of the response
            response_message(str): The response status message
        """

        code: int = 404
        data: str | dict[str, str] = ""

        if isinstance(usr, str):
            return 401, usr

        pix = request.values

        if check := Object(obj=pix.get("pix")):
            code = 401
            with self._db.get_db() as con:
                if self._db._model.pix_rit(con, usr=usr, pix=check.obj):
                    self._db._model.del_pix(con, usr=usr, pix=check.obj)
                code = 201
        return code, data


class Profiles(Socs):
    """
    basic education or acquired skill
    """

    @response
    @authenticate
    def get(self, usr: int | str) -> tuple[int, dict[str, str] | str]:
        """_summary_

        Args:
            usr (int): the user from token authentication
            token_status (Bool): The status of the token, if it is time bound

        Returns:
            response_code(int): The status code of the response
            response_message(str): The response status message
        """

        code: int = 404
        data: str | dict[str, str] = ""

        if isinstance(usr, str):
            return 401, usr

        if not (qs := request.values):
            usr_data = usr

        with self._db.get_db(data_level=1) as con:
            code = 201
            if usr_data:
                data = self._db._model.usr_prof(con, usr=usr)
            elif srch := qs["init"]:
                con = self._db.get_db()
                data = self._db._model.prof_arenz(con, usr=usr)
            elif srch := qs["srch"]:
                data = self._db._model.profs(con, usr=usr, pg=srch)
            elif data_id := qs.get("id"):
                data = self._db._model.prof(con, usr=usr, data_id=data_id)
        return code, data

    @response
    @authenticate
    def delete(self, usr: int | str) -> tuple[int, dict[str, str] | str]:
        """_summary_

        Args:
            usr (int): the user from token authentication
            token_status (Bool): The status of the token, if it is time bound

        Returns:
            response_code(int): The status code of the response
            response_message(str): The response status message
        """

        code: int = 404
        data: str | dict[str, str] = ""

        if isinstance(usr, str):
            return 401, usr

        if not (qs := request.values):
            usr_data = usr

        with self._db.get_db(data_level=1) as con:
            code = 201
            if usr_data:
                data = self._db._model.usr_prof(con, usr=usr)
            elif srch := qs["init"]:
                con = self._db.get_db()
                data = self._db._model.prof_arenz(con, usr=usr)
            elif srch := qs["srch"]:
                data = self._db._model.profs(con, usr=usr, pg=srch)
            elif data_id := qs.get("id"):
                data = self._db._model.prof(con, usr=usr, data_id=data_id)
        return code, data
