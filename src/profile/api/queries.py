"""Module for resolving graph queries"""

from ariadne import QueryType
from flask import request

from setting.dbcon import DbSet as __DBSET
from setting.decs import Auth as authenticate

__DB = __DBSET()
query = QueryType()  # use as decorator for async field resolvers
profs = QueryType()  # use as decorator for async field resolvers


@authenticate
@profs.field("listBase")
async def list_base(usr: int | str) -> dict[str, object]:
    """Fetch list of user's publication resolver for graph queries

    Args:
        usr (int): the user from token authentication

    Returns:
        the created data in payload
        payload(dict): The dict object contains success(key):boolean(value)
        error(key):dict(value) or post(key):dict(value)
    """

    try:
        qs = request.values
        data: list[dict[str, str]] = []

        # data = _db._model.usr_pubs(
        # con, usr=usr
        # )_db._model.data(con, usr=usr, pg=pg)
        async with __DB.get_db() as con:
            if instn := qs.get("instn"):
                async with __DB._model.instn_pubs(con, instn=instn) as cur:
                    data = await cur.fetchall()
            else:
                if qs.get("usr"):
                    usr = qs.get("usr")
                async with __DB._model.usr_pubs(con, usr=usr) as cur:
                    data = await cur.fetchall()

        payload = {"success": True, "posts": data}
    except TypeError as error:
        payload = {"success": False, "errors": [str(error)]}
    return payload


@authenticate
@profs.field("getBase")
async def get_base() -> dict[str, bool | str | dict[str, str]]:
    """Fetch user's basic accademic or skill profile

    Args:
        usr (int): the user from token authentication
        token_status (Bool): The status of the token, if it is time bound

    Returns:
        response_code(int): The status code of the response
        response_message(str): The response status message
    """

    data: str | dict[str, str] = {}
    qs = request.values
    contact = qs["contact"]

    with __DB.get_db() as con:
        if cont := __DB._model.get_cont(con, cnt=contact):
            data = cont
        payload = {"success": True, "posts": data}
    return payload


@authenticate
@profs.field("listAcademic")
async def list_acad(usr: int | str) -> dict[str, object]:
    """Fetch list of user's publication resolver for graph queries

    Args:
        usr (int): the user from token authentication

    Returns:
        the created data in payload
        payload(dict): The dict object contains success(key):boolean(value)
        error(key):dict(value) or post(key):dict(value)
    """

    try:
        qs = request.values
        data: list[dict[str, str]] = []

        # data = _db._model.usr_pubs(
        # con, usr=usr
        # )_db._model.data(con, usr=usr, pg=pg)
        async with __DB.get_db() as con:
            if instn := qs.get("instn"):
                async with __DB._model.instn_pubs(con, instn=instn) as cur:
                    data = await cur.fetchall()
            else:
                if qs.get("usr"):
                    usr = qs.get("usr")
                async with __DB._model.usr_pubs(con, usr=usr) as cur:
                    data = await cur.fetchall()

        payload = {"success": True, "posts": data}
    except TypeError as error:
        payload = {"success": False, "errors": [str(error)]}
    return payload


@authenticate
@profs.field("getAcademic")
async def get_acad(usr: int | str) -> dict[str, bool | str | dict[str, str]]:
    """Fetch user's universal accademic profile

    Args:
        usr (int): the user from token authentication
        token_status (Bool): The status of the token, if it is time bound

    Returns:
        response_code(int): The status code of the response
        response_message(str): The response status message
    """

    data: str | dict[str, str] = {}
    qs = request.values
    contact = qs["contact"]

    with __DB.get_db() as con:
        if cont := __DB._model.get_cont(con, cnt=contact):
            data = cont
        payload = {"success": True, "posts": data}
    return payload


@authenticate
@profs.field("listResearcher")
async def list_researcher(usr: int | str) -> dict[str, object]:
    """Fetch list of user's publication resolver for graph queries

    Args:
        usr (int): the user from token authentication

    Returns:
        the created data in payload
        payload(dict): success(key):boolean(value)
        error(key):dict(value) or post(key):dict(value)
    """

    try:
        qs = request.values
        data: list[dict[str, str]] = []

        # data = _db._model.usr_pubs(
        # con, usr=usr
        # )_db._model.data(con, usr=usr, pg=pg)
        async with __DB.get_db() as con:
            if instn := qs.get("instn"):
                async with __DB._model.instn_pubs(con, instn=instn) as cur:
                    data = await cur.fetchall()
            else:
                if qs.get("usr"):
                    usr = qs.get("usr")
                async with __DB._model.usr_pubs(con, usr=usr) as cur:
                    data = await cur.fetchall()

        payload = {"success": True, "posts": data}
    except TypeError as error:
        payload = {"success": False, "errors": [str(error)]}
    return payload


@authenticate
@profs.field("getResearcher")
async def get_researcher(usr: int | str) -> dict[str, bool | str | dict[str, str]]:
    """Fetch user's Research profile as an accademic

    Args:
        usr (int): the user from token authentication
        token_status (Bool): The status of the token, if it is time bound

    Returns:
        response_code(int): The status code of the response
        response_message(str): The response status message
    """

    data: str | dict[str, str] = {}

    with __DB.get_db(data_level=1) as con:
        if data := __DB._model.usr_reg(con, usr=usr):
            payload = {"success": True, "posts": data}
    return payload


@authenticate
@profs.field("listWork")
async def list_work(usr: int | str) -> dict[str, object]:
    """List event resolver for graph queries

    Args:
        usr (int): the user from token authentication

    Returns:
        the created data in payload
        payload(dict): The dict object contains success(key):boolean(value)
        error(key):dict(value) or post(key):dict(value)
    """

    try:
        qs = request.values
        data: list[dict[str, str]] = []

        async with __DB.get_db() as con:
            if arena := qs.get("arena"):
                async with __DB._model.arena_data(con, arena=arena) as cur:
                    data = await cur.fetchall()
            else:
                async with __DB._model.usr_data(con, usr=usr) as cur:
                    data = await cur.fetchall()

        payload = {"success": True, "posts": data}
    except ValueError as error:
        payload = {"success": False, "errors": [str(error)]}
    return payload


@authenticate
@profs.field("getWork")
async def get_work(usr: int | str) -> dict[str, object]:
    """Fetch user's work profile

    Args:
        usr (int): the user from token authentication
        token_status (Bool): The status of the token, if it is time bound

    Returns:
        response_code(int): The status code of the response
        response_message(str): The response status message
    """

    data: str | dict[str, str] = {}

    with __DB.get_db(data_level=1) as con:
        if data := __DB._model.usr_reg(con, usr=usr):
            payload = {"success": True, "posts": data}
    return payload
