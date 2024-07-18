"""Module for resolving graph queries"""

from ariadne import QueryType
from flask import request

from setting.dbcon import DbSet as __DBSET

__DB = __DBSET()
usrs = QueryType()  # use as decorator for async field resolvers


@usrs.field("listAward")
async def list_award(usr: int | str) -> dict[str, bool | str | dict[str, str]]:
    """List event resolver for graph queries

    Args:
        usr (int): the user from token authentication

    Returns:
        the created data in payload
        payload(dict): The dict object contains success(key):boolean(value)
        error(key):dict(value) or post(key):dict(value)
    """

    data: str | dict[str, str] = {}

    if isinstance(usr, tuple):
        return usr

    if not (qs := request.values):
        usr_data = usr

    with __DB.get_db(data_level=1) as con:
        if usr_data:
            data = __DB._model.usr_awds(con, usr=usr)
        elif data_id := qs.get("id"):
            data = __DB._model.awd(con, data_id=data_id)
        elif srch := qs["srch"]:
            data = __DB._model.awds(con, usr=usr, pg=srch)
    payload = {"success": True, "posts": data}
    return payload


@usrs.field("getAward")
async def get_award(usr: int | str) -> dict[str, bool | str | dict[str, str]]:
    """Fetch a voice resolver for graph queries

    Args:
        usr (int): the user from token authentication

    Returns:
        the created data in payload
        payload(dict): The dict object contains success(key):boolean(value)
        error(key):dict(value) or post(key):dict(value)
    """

    data: str | dict[str, str] = {}

    if isinstance(usr, tuple):
        return usr

    if not (qs := request.values):
        usr_data = usr

    with __DB.get_db(data_level=1) as con:
        if usr_data:
            data = __DB._model.usr_awds(con, usr=usr)
        elif data_id := qs.get("id"):
            data = __DB._model.awd(con, data_id=data_id)
        elif srch := qs["srch"]:
            data = __DB._model.awds(con, usr=usr, pg=srch)
    payload = {"success": True, "posts": data}
    return payload


@usrs.field("listSocial")
async def list_social(usr: int | str) -> dict[str, bool | str | dict[str, str]]:
    """Fetch list of user's publication resolver for graph queries

    Args:
        usr (int): the user from token authentication

    Returns:
        the created data in payload
        payload(dict): The dict object contains success(key):boolean(value)
        error(key):dict(value) or post(key):dict(value)
    """

    data: str | dict[str, str] = {}

    if isinstance(usr, tuple):
        return usr

    if not (qs := request.values):
        usr_data = usr

    with __DB.get_db(data_level=1) as con:
        if usr_data:
            data = __DB._model.usr_socs(con, usr=usr)
        elif srch := qs["srch"]:
            data = __DB._model.socs(con, usr=usr, pg=srch)
        if id := qs.get("id"):  # takes user to social arena
            data = __DB._model.soc(con, usr=usr, id=id)
    payload = {"success": True, "posts": data}
    return payload


@usrs.field("getSocial")
async def get_social(usr: int | str) -> dict[str, bool | str | dict[str, str]]:
    """Fetch a publication resolver for graph queries

    Args:
        usr (int): the user from token authentication

    Returns:
        the created data in payload
        payload(dict): The dict object contains success(key):boolean(value)
        error(key):dict(value) or post(key):dict(value)
    """

    data: str | dict[str, str] = {}

    if isinstance(usr, tuple):
        return usr

    if not (qs := request.values):
        usr_data = usr

    with __DB.get_db(data_level=1) as con:
        if usr_data:
            data = __DB._model.usr_socs(con, usr=usr)
        elif srch := qs["srch"]:
            data = __DB._model.socs(con, usr=usr, pg=srch)
        if id := qs.get("id"):  # takes user to social arena
            data = __DB._model.soc(con, usr=usr, id=id)
    payload = {"success": True, "posts": data}
    return payload


@usrs.field("listProfile")
async def list_profile(usr: int | str) -> dict[str, bool | str | dict[str, str]]:
    """Fetch list of user's publication resolver for graph queries

    Args:
        usr (int): the user from token authentication

    Returns:
        the created data in payload
        payload(dict): The dict object contains success(key):boolean(value)
        error(key):dict(value) or post(key):dict(value)
    """

    data: str | dict[str, str] = {}

    if isinstance(usr, tuple):
        return usr

    if not (qs := request.values):
        usr_data = usr

    with __DB.get_db(data_level=1) as con:
        if usr_data:
            data = __DB._model.usr_socs(con, usr=usr)
        elif srch := qs["srch"]:
            data = __DB._model.socs(con, usr=usr, pg=srch)
        if id := qs.get("id"):  # takes user to social arena
            data = __DB._model.soc(con, usr=usr, id=id)
    payload = {"success": True, "posts": data}
    return payload


@usrs.field("getProfile")
async def get_profile(usr: int | str) -> dict[str, bool | str | dict[str, str]]:
    """Fetch a publication resolver for graph queries

    Args:
        usr (int): the user from token authentication

    Returns:
        the created data in payload
        payload(dict): The dict object contains success(key):boolean(value)
        error(key):dict(value) or post(key):dict(value)
    """

    data: str | dict[str, str] = {}

    if isinstance(usr, tuple):
        return usr

    if not (qs := request.values):
        usr_data = usr

    with __DB.get_db(data_level=1) as con:
        if usr_data:
            data = __DB._model.usr_prof(con, usr=usr)
        elif srch := qs["init"]:
            con = __DB.get_db()
            data = __DB._model.prof_arenz(con, usr=usr)
        elif srch := qs["srch"]:
            data = __DB._model.usrs(con, usr=usr, pg=srch)
        elif data_id := qs.get("id"):
            data = __DB._model.prof(con, usr=usr, data_id=data_id)
    payload = {"success": True, "posts": data}
    return payload
