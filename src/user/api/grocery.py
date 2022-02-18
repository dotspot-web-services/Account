
from flask_restful import Resource
from flask import request
from bleach import clean
from werkzeug import Response

from user.grocerySerializer import Object, CreateAward, CreatePub, CreateSoc
from setting.decs import Auth as authenticate
from setting.dbcon import DbSet
from setting.helper import FileUp, ApiResp


class Awards(Resource):
    """
    User Resource
    """
    def __init__(self) -> None:
        self._db = DbSet(sql_filename="groce.pgsql")

    @authenticate
    def post(self, usr, token_status):

        if isinstance(usr, tuple):
            usr = usr.usr
        elif isinstance(token_status, Response):
            return usr

        awd_data = request.get_json()
        
        if not (check := CreateAward(plc=awd_data.get('plc'), act=awd_data.get('orgsatn'), titl=awd_data.get('ttl'),
            awdt=awd_data.get('dt')
        )):
            return ApiResp(status_code=401)

        with self._db.get_db() as con:
            self._db._model.cr8_awd(
                con, usr=usr, plc=clean(check.plc), acts=clean(check.acts), titl=clean(check.title), 
                awdt=check.awdt
            )
        return ApiResp(status_code=201)

    @authenticate
    def get(self, usr, token_status):
        """reset password"""

        if isinstance(usr, tuple):
            usr = usr.usr
        elif isinstance(token_status, Response):
            return usr

        qs = request.values
        
        if pg := qs["pg"]:
            with self._db.get_db as con:
                data = self._db._model.awds(con, usr=usr, pg=pg)
                return ApiResp(status_code=201, data=data)
        if id := qs.get("id"): 
            with self._db.get_db as con:
                data = self._db._model.awd(con, usr=usr, id=id)
                return ApiResp(status_code=201, data=data)
        else:
            with self._db.get_db as con:
                data = self._db._model.awds(con, usr=usr)
                return ApiResp(status_code=201, data=data)
    
    @authenticate
    def put(self, usr, token_status):
        # get the post data

        if isinstance(usr, tuple):
            usr = usr.usr
        elif isinstance(token_status, Response):
            return usr

        awd_data = request.get_json()

        if not (check := CreateAward(plc=awd_data.get('plc'), act=awd_data.get('orgsatn'), titl=awd_data.get('ttl'),
            awdt=awd_data.get('dt'), awd=awd_data.get('award')
        )):
            return ApiResp(status_code=401)
        with self._db.get_db() as con:
            if self._db._model.awd_rit(
                con, usr=usr, awd=check.obj
            ):
                return ApiResp(status_code=401)
            elif self._db._model.cr8_awd(
                con, usr=usr, plc=clean(check.plc), acts=clean(check.acts), titl=clean(check.title), 
                awdt=check.awdt
            ):
                return ApiResp(status_code=201)
            else:
                return ApiResp(status_code=401)

    @authenticate
    def delete(self, usr, token_status):
        """reset password"""

        if isinstance(usr, tuple):
            usr = usr.usr
        elif isinstance(token_status, Response):
            return usr

        awd = request.values

        if not (check := Object(plc=awd.get('awd'))):
            return ApiResp(status_code=401)
        with self._db.get_db() as con:
            if self._db._model.awd_rit(con, usr=usr, awd=check.obj):
                return ApiResp(status_code=401)
            elif self._db._model.del_awd(con, usr=usr, awd=check.obj):
                return ApiResp(status_code=201)
            else:
                return ApiResp(status_code=401)
    
    def options(self):
        return {'Allow' : ['POST', 'GET']}, 200, \
        {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods' : '*',
        'Access-Control-Allow-Headers': '*', 'cross-site-cookies': 'session', 
        'samesite': 'Lax'}

class Pubs(Awards):
    """get all events with get request and insert event with post request"""

    @authenticate
    def post(self, usr, token_status):

        if isinstance(usr, tuple):
            usr = usr.usr
        elif isinstance(token_status, Response):
            return usr

        pub_data = request.get_json()
        
        if not (check := CreatePub(rsrch=pub_data.get('org'), dfld=pub_data.get('fld'), dttl=pub_data.get('titl'),
            fyl=pub_data.get('fyl'), pdt=pub_data.get('pdt')
        )):
            return ApiResp(status_code=401)

        with self._db.get_db() as con:
            self._db._model.cr8_pub(con, usr=usr, srch=check.instn, fld=clean(check.dfld), ttl=clean(check.dttl), 
                fyl=check.med, pdt=check.pdt
            )
        return ApiResp(status_code=201)
    
    @authenticate
    def get(self, usr, token_status):
        """reset password"""

        if isinstance(usr, tuple):
            usr = usr.usr
        elif isinstance(token_status, Response):
            return usr

        qs = request.values
        
        if pg := qs["pg"]:
            with self._db.get_db as con:
                data = self._db._model.pubs(con, usr=usr, pg=pg)
                return ApiResp(status_code=201, data=data)
        if id := qs.get("id"): 
            with self._db.get_db as con:
                data = self._db._model.pub(con, usr=usr, id=id)
                return ApiResp(status_code=201, data=data)
        else:
            with self._db.get_db as con:
                data = self._db._model.pubs(con, usr=usr)
                return ApiResp(status_code=201, data=data)

    
    @authenticate
    def put(self, usr, token_status):
        # get the post data

        if isinstance(usr, tuple):
            usr = usr.usr
        elif isinstance(token_status, Response):
            return usr

        pub_data = request.get_json()

        if not (check := CreatePub(rsrch=pub_data.get('org'), dfld=pub_data.get('fld'), dttl=pub_data.get('titl'),
            fyl=pub_data.get('fyl'), pdt=pub_data.get('pdt'), pub=pub_data.get('pub')
        )):
            return ApiResp(status_code=401)
        with self._db.get_db() as con:
            if self._db._model.pub_rit(con, usr=usr, awd=check.obj):
                return ApiResp(status_code=401)
            elif self._db._model.upd8_pub(con, usr=usr, srch=check.instn, fld=clean(check.dfld), ttl=clean(check.dttl), 
                fyl=check.med, pdt=check.pdt
            ):
                return ApiResp(status_code=201)
            else:
                return ApiResp(status_code=401)

    @authenticate
    def delete(self, usr, token_status):
        """reset password"""

        if isinstance(usr, tuple):
            usr = usr.usr
        elif isinstance(token_status, Response):
            return usr

        pub = request.values

        if not (check := Object(obj=pub.get('pub'))):
            return ApiResp(status_code=401)
        with self._db.get_db() as con:
            if self._db._model.pub_rit(con, usr=usr, awd=check.obj):
                return ApiResp(status_code=401)
            elif self._db._model.del_pub(con, usr=usr, pub=check.obj):
                return ApiResp(status_code=201)
            else:
                return ApiResp(status_code=401)

class Socs(Pubs):
    """API for all hubbies or interests outside studies"""

    def __init__(self):
        self._db = DbSet()

    @authenticate
    def post(self, usr, token_status):

        if isinstance(usr, tuple):
            usr = usr.usr
        elif isinstance(token_status, Response):
            return usr

        soc_data = request.get_json()
        
        if not (check := CreateSoc(titl=soc_data.get('titl'), typ=soc_data.get('typ'))):
            return ApiResp(status_code=401)
        with self._db.get_db() as con:
            self._db._model.cr8_soc(con, usr=usr, typ=clean(check.typ), ttl=clean(check.title))
        return ApiResp(status_code=201)

    @authenticate
    def get(self, usr, token_status):
        """reset password"""

        if isinstance(usr, tuple):
            usr = usr.usr
        elif isinstance(token_status, Response):
            return usr

        qs = request.values
        
        if pg := qs["pg"]:
            with self._db.get_db as con:
                data = self._db._model.socs(con, usr=usr, pg=pg)
                return ApiResp(status_code=201, data=data)
        if id := qs.get("id"): 
            with self._db.get_db as con:
                data = self._db._model.soc(con, usr=usr, id=id)
                return ApiResp(status_code=201, data=data)
        else:
            with self._db.get_db as con:
                data = self._db._model.socs(con, usr=usr)
                return ApiResp(status_code=201, data=data)

    @authenticate
    def put(self, usr, token_status):
        # get the post data

        if isinstance(usr, tuple):
            usr = usr.usr
        elif isinstance(token_status, Response):
            return usr

        soc_data = request.get_json()

        if not (check := CreateSoc(titl=soc_data.get('titl'), typ=soc_data.get('typ'))):
            return ApiResp(status_code=401)

        with self._db.get_db() as con:
            if self._db._model.soc_rit(con, usr=usr, awd=check.obj):
                return ApiResp(status_code=401)
            elif self._db._model.upd8_soc(con, usr=usr, typ=clean(check.typ), ttl=clean(check.title)):
                return ApiResp(status_code=201)
            else:
                return ApiResp(status_code=401)

    @authenticate
    def delete(self, usr, token_status):
        """reset password"""

        if isinstance(usr, tuple):
            usr = usr.usr
        elif isinstance(token_status, Response):
            return usr

        soc = request.values

        if not (check := Object(obj=soc.get('soc'))):
            return ApiResp(status_code=401)
        with self._db.get_db() as con:
            if self._db._model.soc_rit(con, usr=usr, soc=check.obj):
                return ApiResp(status_code=401)
            elif self._db._model.del_soc(con, usr=usr, soc=check.obj):
                return ApiResp(status_code=201)
            else:
                return ApiResp(status_code=401)


class Avatars(Socs):
    """
    basic education or acquired skill
    """

    @authenticate
    def post(self, usr, token_status):

        if isinstance(usr, tuple):
            usr = usr.usr
        elif isinstance(token_status, Response):
            return usr

        file = request.files['file']
        print(file)

        if not (check:= FileUp(file=file)):
            return ApiResp(status_code=401)

        with self._db.get_db() as con:
            self._db._model.cr8_pix(con, medfor=usr, file_path=check)
        return ApiResp(status_code=201)

    @authenticate
    def get(self, usr, token_status):
        """reset password"""

        if isinstance(usr, tuple):
            usr = usr.usr
        elif isinstance(token_status, Response):
            return usr

        qs = request.values
        
        if pg := qs["pg"]:
            with self._db.get_db as con:
                data = self._db._model.pix(con, usr=usr, pg=pg)
                return ApiResp(status_code=201, data=data)
        if id := qs.get("id"): 
            with self._db.get_db as con:
                data = self._db._model.pixs(con, usr=usr, id=id)
                return ApiResp(status_code=201, data=data)
        else:
            with self._db.get_db as con:
                data = self._db._model.pix(con, usr=usr)
                return ApiResp(status_code=201, data=data)

    @authenticate
    def delete(self, usr, token_status):
        """reset password"""

        if isinstance(usr, tuple):
            usr = usr.usr
        elif isinstance(token_status, Response):
            return usr

        pix = request.values

        if not (check := Object(obj=pix.get('pix'))):
            return ApiResp(status_code=401)
        with self._db.get_db() as con:
            if self._db._model.pix_rit(con, usr=usr, pix=check.obj):
                return ApiResp(status_code=401)
            elif self._db._model.del_pix(con, usr=usr, pix=check.obj):
                return ApiResp(status_code=201)
            else:
                return ApiResp(status_code=401)

class Profiles(Socs):
    """
    basic education or acquired skill
    """

    @authenticate
    def get(self, usr, token_status):
        """reset password"""

        if isinstance(usr, tuple):
            usr = usr.usr
        elif isinstance(token_status, Response):
            return usr

        qs = request.values
        
        if pg := qs["pg"]:
            with self._db.get_db as con:
                data = self._db._model.pix(con, usr=usr, pg=pg)
                return ApiResp(status_code=201, data=data)
        if id := qs.get("id"): 
            with self._db.get_db as con:
                data = self._db._model.pixs(con, usr=usr, id=id)
                return ApiResp(status_code=201, data=data)
        else:
            with self._db.get_db as con:
                data = self._db._model.pix(con, usr=usr)
                return ApiResp(status_code=201, data=data)
