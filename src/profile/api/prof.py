"""User profile resources"""

from profile.profSerializer import Acads, Basics, Object, Place, Resrch
from typing import Dict, TypeVar

from bleach import clean
from flask import request
from flask_restful import Resource
from pydantic import ValidationError

from setting.dbcon import DbSet
from setting.decs import Auth as authenticate
from setting.decs import Responders as response
from setting.helper import convert_errors

T = TypeVar("T", int, Dict[str, str])


class Basic(Resource):
    """
    basic education or acquired skill
    """

    def __init__(self) -> None:
        self._db = DbSet(sql_filename="prof.pgsql")

    @response
    @authenticate
    def post(self, usr: int | str) -> tuple[int, dict[str, str] | str]:
        """Register user's basic accademic or skill profile

        Args:
            usr (int): the user from token authentication
            token_status (Bool): The status of the token, if it is time bound

        Returns:
            response_code(int): The status code of the response
            response_message(str): The response status message
        """

        code: int = 422
        data: str | dict[str, str] = ""

        # get the post data
        if isinstance(usr, str):
            return 401, usr

        try:
            bsic_data = request.get_json()
            check = Basics(
                fld=bsic_data.get("fld"),
                locatn=bsic_data.get("locatn"),
                strt=bsic_data.get("strt"),
                end=bsic_data.get("end"),
                acad=bsic_data.get("acad"),
            )
        except ValidationError as err:
            data = convert_errors(err=err)
            return code, data

        with self._db.get_db() as con:
            self._db._model.cr8_base(
                con,
                usr=usr,
                dspln=clean(check.fld),
                plc=clean(check.locatn),
                strtd=check.strt,
                endd=check.end,
                typ=check.acad,
            )
            code = 201
        return code, data

    @response
    @authenticate
    def get(self, usr: int | str) -> tuple[int, dict[str, str] | str]:
        """Fetch user's basic accademic or skill profile

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

        with self._db.get_db(data_level=1) as con:
            if id := request.values.get("base"):
                data = self._db._model.base(con, usr=usr, id=id)
                code = 200
            elif usr:
                data = self._db._model.usr_base(con, usr=usr)
                code = 200
            # elif srch := qs.get("srch"): # this goes with search
            #    data = self._db._model.bases(con, usr=usr, pg=srch)
            #    return 201, data
        return code, data

    @response
    @authenticate
    def put(self, usr: int | str) -> tuple[int, dict[str, str] | str]:
        """Update user's basic accademic or skill profile

        Args:
            usr (int): the user from token authentication
            token_status (Bool): The status of the token, if it is time bound

        Returns:
            response_code(int): The status code of the response
            response_message(str): The response status message
        """

        code: int = 422
        data: str | dict[str, str] = ""

        # get the post data
        if isinstance(usr, str):
            return 401, usr

        try:
            bsic_data = request.get_json()
            check = Basics(
                fld=bsic_data.get("fld"),
                locatn=bsic_data.get("locatn"),
                strt=bsic_data.get("strt"),
                end=bsic_data.get("end"),
                acad=bsic_data.get("acad"),
            )
        except ValidationError as err:
            data = convert_errors(err=err)
            return code, data

        with self._db.get_db() as con:
            code = 404
            if not self._db._model.base_rit(con, usr=usr, base=check.obj):
                code = 401
                data = self._failed_rits
            if self._db._model.upd8_base(
                con,
                usr=usr,
                dspln=clean(check.fld),
                plc=clean(check.locatn),
                strtd=check.strt,
                endd=check.end,
                typ=check.acad,
            ):
                code = 201
        return code, data

    @response
    @authenticate
    def delete(self, usr: int | str) -> tuple[int, dict[str, str] | str]:
        """Delete user's basic accademic or skill profile

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
        base = request.values

        if not (check := Object(obj=base.get("base"))):
            code = 404
            return code, data
        with self._db.get_db() as con:
            if self._db._model.base_rit(con, usr=usr, soc=check.obj):
                data = self._failed_rits
            elif self._db._model.del_base(con, usr=usr, soc=check.obj):
                code = 200
        return code, data

    def options(self) -> tuple[dict[str, list[str]], int, dict[str, str]]:
        """Cross origin setter operations"""

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


class Accademics(Basic):
    """
    User Login Resource
    """

    @response
    @authenticate
    def post(self, usr: int | str) -> tuple[int, dict[str, str] | str]:
        """Register user's basic universal accademic profile
        Check the user's basic accademic profile if qualified

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
            acad_data = request.get_json()
            check = Acads(
                fld=acad_data.get("fld"),
                loctn=acad_data.get("locatn"),
                ttl=acad_data.get("ttl"),
                strt=acad_data.get("strt"),
                end=acad_data.get("end"),
            )
        except ValidationError as err:
            data = convert_errors(err=err)
            return code, data

        with self._db.get_db() as con:
            code = 401
            data = self._failed_rits
            if base := self._db._model.acadqfn(con, usr=usr):
                self._db._model.cr8_acad(
                    con,
                    usr=usr,
                    dspln=clean(check.fld),
                    plc=clean(check.locatn),
                    stg=clean(check.ttl),
                    base=base,
                    strtd=check.strt,
                    endd=check.end,
                )
                code = 201
        return code, data

    @response
    @authenticate
    def get(self, usr: int | str) -> tuple[int, dict[str, str] | str]:
        """Fetch user's universal accademic profile

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

        with self._db.get_db(data_level=1) as con:
            code = 404

            if id := request.values.get("acad"):
                data = self._db._model.acada(con, usr=usr, id=id)
                code = 200
            elif usr:
                data = self._db._model.usr_acada(con, usr=usr)
                code = 200
            # elif srch := qs.get("srch"):
            #    data = self._db._model.acadas(con, usr=usr, pg=srch)
            #    return 201, data
        return code, data

    @response
    @authenticate
    def put(self, usr: int | str) -> tuple[int, dict[str, str] | str] | int:
        """Update user's basic universal accademic profile if existing record

        Args:
            usr (int): the user from token authentication
            token_status (Bool): The status of the token, if it is time bound

        Returns:
            response_code(int): The status code of the response
            response_message(str): The response status message
        """
        # get the post data

        code: int = 422
        data: str | dict[str, str] = ""

        if isinstance(usr, str):
            return 401, usr

        try:
            acad_data = request.get_json()
            check = Acads(
                fld=acad_data.get("fld"),
                locatn=acad_data.get("locatn"),
                ttl=acad_data.get("ttl"),
                strt=acad_data.get("strt"),
                end=acad_data.get("end"),
            )
        except ValidationError as err:
            data = convert_errors(err=err)
            return code, data

        with self._db.get_db() as con:
            code = 404
            if not self._db._model.upd8_acad(
                con,
                usr=usr,
                dspln=clean(check.fld),
                plc=clean(check.locatn),
                stg=clean(check.ttl),
                strtd=check.strt,
                endd=check.end,
            ):
                return 201
        return code, data

    @response
    @authenticate
    def delete(self, usr: int | str) -> tuple[int, dict[str, str] | str]:
        """Delete user's basic universal accademic profile

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
        acad = request.values

        if check := Object(obj=acad.get("acad")):
            with self._db.get_db() as con:
                if not self._db._model.acad_rit(con, usr=usr, soc=check.obj):
                    code = 401
                elif self._db._model.del_acad(con, usr=usr, soc=check.obj):
                    code = 200
        return code, data


class Resacher(Accademics):
    """
    Logout Resource
    """

    @response
    @authenticate
    def post(self, usr: int | str) -> tuple[int, dict[str, str] | str]:
        """Register user's Research profile as an accademic

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
            rsrcha = request.get_json()
            check = Resrch(
                fld=rsrcha.get("fld"),
                locatn=rsrcha.get("locatn"),
                typ=rsrcha.get("typ"),
                emel=rsrcha.get("emel"),
                strt=rsrcha.get("strt"),
                end=rsrcha.get("end"),
            )
        except ValidationError as err:
            data = convert_errors(err=err)
            return code, data

        with self._db.get_db() as con:
            code = 401
            data = self._failed_rits
            if acad := self._db._model.rsrchaqfn(con, usr=usr):
                self._db._model.cr8_srcha(
                    con,
                    usr=usr,
                    cnt=check.emel,
                    base=acad,
                    org=check.locatn,
                    dspln=check.fld,
                    typ=check.typ,
                    strtd=check.strt,
                    endd=check.end,
                )
                code = 201
                data = ""
        return code, data

    @response
    @authenticate
    def get(self, usr: int | str) -> tuple[int, dict[str, str] | str]:
        """Fetch user's Research profile as an accademic

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

        with self._db.get_db(data_level=1) as con:
            if data_id := request.values.get("id"):
                data = self._db._model.srcha(con, usr=usr, data_id=data_id)
                code = 200
            elif usr:
                data = self._db._model.rsrcha(con, usr=usr)
                code = 200
            # elif srch := qs["srch"]:
            #    data = self._db._model.srchas(con, usr=usr, pg=srch)
            #    return 201, data
        return code, data

    @response
    @authenticate
    def put(self, usr: int | str) -> tuple[int, dict[str, str] | str]:
        """Update user's Research profile as an accademic if existing profile
        Args:
            usr (int): the user from token authentication
            token_status (Bool): The status of the token, if it is time bound

        Returns:
            response_code(int): The status code of the response
            response_message(str): The response status message
        """
        # get the post data

        code: int = 422
        data: str | dict[str, str] = ""

        if isinstance(usr, str):
            return 401, usr

        try:
            rsrcha = request.get_json()
            check = Resrch(
                fld=rsrcha.get("fld"),
                locatn=rsrcha.get("locatn"),
                typ=rsrcha.get("typ"),
                emel=rsrcha.get("emel"),
                strt=rsrcha.get("strt"),
                end=rsrcha.get("end"),
            )
        except ValidationError as err:
            data = convert_errors(err=err)
            code = 422
            return code, data

        with self._db.get_db() as con:
            self._db._model.upd8_srcha(
                con,
                usr=usr,
                cnt=check.emel,
                org=clean(check.locatn),
                dspln=clean(check.fld),
                typ=check.typ,
                strtd=check.strt,
                endd=check.end,
            )
            code = 201
        return code, data

    @response
    @authenticate
    def delete(self, usr: int | str) -> tuple[int, dict[str, str] | str]:
        """Delete user's Research profile as an accademic

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
        srcha = request.values

        if not (check := Object(obj=srcha.get("srcha"))):
            return code, data
        with self._db.get_db() as con:
            code = 401
            if self._db._model.srcha_rit(con, usr=usr, soc=check.obj):
                self._db._model.del_srcha(con, usr=usr, soc=check.obj)
                code = 200
        return code, data


class Works(Resacher):
    """
    basic education or acquired skill
    """

    @response
    @authenticate
    def post(self, usr: int | str) -> tuple[int, dict[str, str] | str]:
        """Register user's work profile
        Args:
            usr (int): the user from token authentication
            token_status (Bool): The status of the token, if it is time bound

        Returns:
            response_code(int): The status code of the response
            response_message(str): The response status message
        """
        # get the post data

        code: int = 422
        data: str | dict[str, str] = ""

        if isinstance(usr, str):
            return 401, usr

        try:
            wrk_data = request.get_json()
            check = Place(
                fld=wrk_data.get("fld"),
                locatn=wrk_data.get("locatn"),
                strt=wrk_data.get("strt"),
                end=wrk_data.get("end"),
            )
        except ValidationError as err:
            data = convert_errors(err=err)
            return code, data

        with self._db.get_db() as con:
            self._db._model.cr8_wrk(
                con,
                usr=usr,
                plc=clean(check.locatn),
                dng=clean(check.fld),
                strtd=check.strt,
                endd=check.end,
            )
            code = 201
        return code, data

    @response
    @authenticate
    def get(self, usr: int | str) -> tuple[int, dict[str, str] | str]:
        """Fetch user's work profile

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

        with self._db.get_db(data_level=1) as con:
            if data_id := request.values.get("id"):
                data = self._db._model.wrk(con, usr=usr, data_id=data_id)
                code = 200
            if usr:
                data = self._db._model.usr_wrk(con, usr=usr)
                code = 200
            # elif srch := qs["srch"]:
            #    data = self._db._model.wrks(con, usr=usr, pg=srch)
            #    return 201, data
        return code, data

    @response
    @authenticate
    def put(self, usr: int | str) -> tuple[int, dict[str, str] | str]:
        """Update user's work profile if existing record

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
            wrk_data = request.get_json()
            check = Place(
                fld=wrk_data.get("fld"),
                locatn=wrk_data.get("locatn"),
                strt=wrk_data.get("strt"),
                end=wrk_data.get("end"),
            )
        except ValidationError as err:
            data = convert_errors(err=err)
            return code, data

        with self._db.get_db() as con:
            if not self._db._model.upd8_wrk(
                con,
                usr=usr,
                plc=clean(check.locatn),
                dng=clean(check.fld),
                strtd=check.strt,
                endd=check.end,
            ):
                code = 201
        return code, data

    @response
    @authenticate
    def delete(self, usr: int | str) -> tuple[int, dict[str, str] | str]:
        """Delete user's work profile

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
        wrk = request.values

        if not (check := Object(obj=wrk.get("wrk"))):
            return code, data
        with self._db.get_db() as con:
            code = 401
            data = self._failed_rits
            if self._db._model.wrk_rit(con, usr=usr, soc=check.obj):
                self._db._model.del_wrk(con, usr=usr, soc=check.obj)
                code = 200
        return code, data
