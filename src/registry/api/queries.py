"""Module for resolving graph queries"""

from ariadne import QueryType
from flask import request

from setting.dbcon import DbSet as __DBSET
from setting.decs import Auth as authenticate

__DB = __DBSET()
query = QueryType()  # use as decorator for async field resolvers
accs = QueryType()  # use as decorator for async field resolvers


@authenticate
@accs.field("listAccount")
async def list_account(usr: int | str) -> dict[str, bool | str | dict[str, str]]:
    """Fetch list of user's publication resolver for graph queries

    Args:
        usr (int): the user from token authentication

    Returns:
        the created data in payload
        payload(dict): success(key):boolean(value)
        error(key):dict(value) or post(key):dict(value)
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
@accs.field("getAccount")
async def get_Account(usr: int | str) -> dict[str, bool | str | dict[str, str]]:
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


logs = QueryType()  # use as decorator for async field resolvers


@authenticate
@logs.field("listLog")
async def list_log(usr: int | str) -> dict[str, object]:
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
        pubs: list[dict[str, str]] = []

        # data = _db._model.usr_pubs(
        # con, usr=usr
        # )_db._model.pubs(con, usr=usr, pg=pg)
        async with __DB.get_db() as con:
            if instn := qs.get("instn"):
                async with __DB._model.instn_pubs(con, instn=instn) as cur:
                    pubs = await cur.fetchall()
            else:
                if qs.get("usr"):
                    usr = qs.get("usr")
                async with __DB._model.usr_pubs(con, usr=usr) as cur:
                    pubs = await cur.fetchall()

        payload = {"success": True, "posts": pubs}
    except TypeError as error:
        payload = {"success": False, "errors": [str(error)]}
    return payload


@authenticate
@logs.field("getLog")
async def get_log(usr: int | str) -> dict[str, bool | str | dict[str, str]]:
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


reset = QueryType()  # use as decorator for async field resolvers


@authenticate
@reset.field("listReset")
async def list_reset(usr: int | str) -> dict[str, object]:
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
        pubs: list[dict[str, str]] = []

        # data = _db._model.usr_pubs(
        # con, usr=usr
        # )_db._model.pubs(con, usr=usr, pg=pg)
        async with __DB.get_db() as con:
            if instn := qs.get("instn"):
                async with __DB._model.instn_pubs(con, instn=instn) as cur:
                    pubs = await cur.fetchall()
            else:
                if qs.get("usr"):
                    usr = qs.get("usr")
                async with __DB._model.usr_pubs(con, usr=usr) as cur:
                    pubs = await cur.fetchall()

        payload = {"success": True, "posts": pubs}
    except TypeError as error:
        payload = {"success": False, "errors": [str(error)]}
    return payload


@authenticate
@reset.field("getReset")
async def get_reset(usr: int | str) -> dict[str, bool | str | dict[str, str]]:
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
