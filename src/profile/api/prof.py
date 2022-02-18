
from flask_restful import Resource
from flask import request
from bleach import clean
from werkzeug import Response

from profile.profSerializer import Object, Basics, Resrch, Place, Acads
from setting.decs import Auth as authenticate
from setting.dbcon import DbSet
from setting.helper import ApiResp


class Basic(Resource):
    """
    basic education or acquired skill
    """

    def __init__(self):
        self._db = DbSet(sql_filename="prof.pgsql")

    @authenticate
    def post(self, usr, token_status):
        # get the post data

        if isinstance(usr, tuple):
            usr = usr.usr
        elif isinstance(token_status, Response):
            return usr
        bsic_data = request.get_json()

        if not (check:= Basics(dspln=bsic_data.get('displn'), place=bsic_data.get('plc'), strtd=bsic_data.get('strt'), 
                endd=bsic_data.get('end'),  acad=bsic_data.get('typ')
            )):
            return ApiResp(status_code=401)
        
        with self._db.get_db() as con:
            self._db._model.cr8_base(con, usr=usr, dspln=clean(check.dspln), plc=clean(check.place), 
                strtd=check.strtd, endd=check.endd, typ=check.acad
            )
            return ApiResp(status_code=201)

    @authenticate
    def get(self, usr, token_status):

        if isinstance(usr, tuple):
            usr = usr.usr
        elif isinstance(token_status, Response):
            return usr

        qs = request.values

        if pg := qs["pg"]:
            with self._db.get_db as con:
                data = self._db._model.bases(con, usr=usr, pg=pg)
                return ApiResp(status_code=201, data=data)
        if id := qs.get("id"): 
            with self._db.get_db as con:
                data = self._db._model.base(con, usr=usr, id=id)
                return ApiResp(status_code=201, data=data)
        else:
            with self._db.get_db as con:
                data = self._db._model.bases(con, usr=usr)
                return ApiResp(status_code=201, data=data)

    @authenticate
    def put(self, usr, token_status):
        # get the post data

        if isinstance(usr, tuple):
            usr = usr.usr
        elif isinstance(token_status, Response):
            return usr

        bsic_data = request.get_json()

        if not (check := Basics(dspln=bsic_data.get('displn'), place=bsic_data.get('plc'), strtd=bsic_data.get('strt'), 
                endd=bsic_data.get('end'),  acad=bsic_data.get('typ')
            )):
            return ApiResp(status_code=401)
        with self._db.get_db() as con:
            if self._db._model.base_rit(con, usr=usr, base=check.obj):
                return ApiResp(status_code=401)
            if not self._db._model.upd8_base(con, usr=usr, dspln=clean(check.dspln), plc=clean(check.place), 
                strtd=check.strtd, endd=check.endd, typ=check.acad
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

        base = request.values

        if not (check := Object(obj=base.get('soc'))):
            return ApiResp(status_code=401)
        with self._db.get_db() as con:
            if self._db._model.base_rit(con, usr=usr, soc=check.obj):
                return ApiResp(status_code=401)
            elif self._db._model.del_base(con, usr=usr, soc=check.obj):
                return ApiResp(status_code=201)
            else:
                return ApiResp(status_code=401)

    def options(self):
        return {'Allow' : ['POST', 'GET']}, 200, \
        {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods' : '*',
        'Access-Control-Allow-Headers': '*', 'cross-site-cookies': 'session', 
        'samesite': 'Lax'}

class Accademics(Basic):
    """
    User Login Resource
    """

    @authenticate
    def post(self, usr, token_status):
        # get the post data
        if isinstance(usr, tuple):
            usr = usr.usr
        elif isinstance(token_status, Response):
            return usr
        acad_data = request.get_json()

        if not (check := Acads(
                dspln=acad_data.get('displn'), place=acad_data.get('plc'),
                ttl=acad_data.get('ttl'), strtd=acad_data.get('strt'), endd=acad_data.get('end')
            )):
            return ApiResp(status_code=401)

        with self._db.get_db() as con:
            if not (base:= self._db._model.acadqfn(con, usr=usr)):
                return ApiResp(status_code=401)
            self._db._model.cr8_acad(
                con, usr=usr, dspln=clean(check.dspln), plc=clean(check.place),  
                base=base, stg=clean(check.ttl), strtd=check.strtd, endd=check.endd,
            )
            return ApiResp(status_code=201)

    @authenticate
    def get(self, usr, token_status):
        """get accademics data"""

        if isinstance(usr, tuple):
            usr = usr.usr
        elif isinstance(token_status, Response):
            return usr

        qs = request.values
        
        if pg := qs["pg"]:
            with self._db.get_db as con:
                data = self._db._model.acadas(
                con, usr=usr, pg=pg
            )
                return ApiResp(status_code=201, data=data)
        if id := qs.get("id"): 
            with self._db.get_db as con:
                data = self._db._model.acada(
                con, usr=usr, id=id
            )
                return ApiResp(status_code=201, data=data)
        else:
            with self._db.get_db as con:
                data = self._db._model.acadas(
                con, usr=usr
            )
                return ApiResp(status_code=201, data=data)

    @authenticate
    def put(self, usr, token_status):
        # get the post data

        if isinstance(usr, tuple):
            usr = usr.usr
        elif isinstance(token_status, Response):
            return usr

        acad_data = request.get_json()

        print(usr)
        
        if not (check := Acads(
                dspln=acad_data.get('displn'), place=acad_data.get('plc'),
                ttl=acad_data.get('ttl'), strtd=acad_data.get('strt'), endd=acad_data.get('end')
            )):
            return ApiResp(status_code=401)
        with self._db.get_db() as con:
            if not self._db._model.upd8_acad(
                con, usr=usr, dspln=clean(check.dspln), plc=clean(check.place),  
                stg=clean(check.ttl), strtd=check.strtd, endd=check.endd,
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

        acad = request.values
        
        if not (check := Object(obj=acad.get('acad'))):
            return ApiResp(status_code=401)
        with self._db.get_db() as con:
            if self._db._model.acad_rit(con, usr=usr, soc=check.obj):
                return ApiResp(status_code=401)
            elif self._db._model.del_acad(con, usr=usr, soc=check.obj):
                return ApiResp(status_code=201)
            else:
                return ApiResp(status_code=401)

class Resacher(Accademics):
    """
    Logout Resource
    """
    
    @authenticate
    def post(self, usr, token_status):
        # get the post data
        if isinstance(usr, tuple):
            usr = usr.usr
        elif isinstance(token_status, Response):
            return usr
        rsrch_data = request.get_json()

        if not (check:= Resrch(
                typ=rsrch_data.get('typ'), place=rsrch_data.get('plc'), dspln=rsrch_data.get('displn'), 
                email=rsrch_data.get('emel'), strtd=rsrch_data.get('strt'), endd=rsrch_data.get('end')
            )):
            return ApiResp(status_code=401)

        with self._db.get_db() as con:
            if not (acad:= self._db._model.rsrchaqfn(con, usr=usr)):
                return ApiResp(status_code=401)
            self._db._model.cr8_srcha(
                con, usr=usr, cnt=check.email, base=acad, org=clean(check.place), 
                dspln=clean(check.dspln), typ=check.typ, strtd=check.strtd, endd=check.endd
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
                data = self._db._model.rsrchs(
                con, usr=usr, pg=pg
            )
                return ApiResp(status_code=201, data=data)
        if id := qs.get("id"): 
            with self._db.get_db as con:
                data = self._db._model.rsrcha(
                con, usr=usr, id=id
            )
                return ApiResp(status_code=201, data=data)
        else:
            with self._db.get_db as con:
                data = self._db._model.rsrchs(
                con, usr=usr
            )
                return ApiResp(status_code=201, data=data)

    @authenticate
    def put(self, usr, token_status):
        # get the post data

        if isinstance(usr, tuple):
            usr = usr.usr
        elif isinstance(token_status, Response):
            return usr

        rsrch_data = request.get_json()

        if not (check := Resrch(
                typ=rsrch_data.get('typ'), place=rsrch_data.get('plc'), dspln=rsrch_data.get('displn'), 
                email=rsrch_data.get('emel'), strtd=rsrch_data.get('strt'), endd=rsrch_data.get('end')
            )):
            return ApiResp(status_code=401)
        with self._db.get_db() as con:
            if not self._db._model.upd8_srcha(
                con, usr=usr, cnt=check.email, org=clean(check.place), dspln=clean(check.dspln), 
                typ=check.typ, strtd=check.strtd, endd=check.endd
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

        srcha = request.values
        
        if not (check := Object(obj=srcha.get('srcha'))):
            return ApiResp(status_code=401)
        with self._db.get_db() as con:
            if self._db._model.srcha_rit(con, usr=usr, soc=check.obj):
                return ApiResp(status_code=401)
            elif self._db._model.del_srcha(con, usr=usr, soc=check.obj):
                return ApiResp(status_code=201)
            else:
                return ApiResp(status_code=401)

class Works(Resacher):
    """
    basic education or acquired skill
    """

    @authenticate
    def post(self, usr, token_status):
        # get the post data

        if isinstance(usr, tuple):
            usr = usr.usr
        elif isinstance(token_status, Response):
            return usr

        wrk_data = request.get_json()

        if not (check:= Place(
                    dspln=wrk_data.get('displn'), place=wrk_data.get('plc'),
                    strtd=wrk_data.get('strt'), endd=wrk_data.get('end')
                )):
            return ApiResp(status_code=401)

        with self._db.get_db() as con:
            self._db._model.cr8_wrk(
                con, usr=usr, plc=clean(check.place), dng=clean(check.dspln), strtd=check.strtd, endd=check.endd
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
                data = self._db._model.wrks(
                con, usr=usr, pg=pg
            )
                return ApiResp(status_code=201, data=data)
        if id := qs.get("id"): 
            with self._db.get_db as con:
                data = self._db._model.wrk(
                con, usr=usr, id=id
            )
                return ApiResp(status_code=201, data=data)
        else:
            with self._db.get_db as con:
                data = self._db._model.wrks(
                con, usr=usr
            )
                return ApiResp(status_code=201, data=data)

    @authenticate
    def put(self, usr, token_status):
        # get the post data

        if isinstance(usr, tuple):
            usr = usr.usr
        elif isinstance(token_status, Response):
            return usr

        wrk_data = request.get_json()

        if not (check := Place(dspln=wrk_data.get('displn'), place=wrk_data.get('plc'),
                strtd=wrk_data.get('strt'), endd=wrk_data.get('end')
            )):
            return ApiResp(status_code=401)
        with self._db.get_db() as con:
            if not self._db._model.upd8_wrk(
                con, usr=usr, plc=clean(check.place), dng=clean(check.dspln), strtd=check.strtd, endd=check.endd
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

        wrk = request.values
        
        if not (check := Object(obj=wrk.get('wrk'))):
            return ApiResp(status_code=401)
        with self._db.get_db() as con:
            if self._db._model.wrk_rit(con, usr=usr, soc=check.obj):
                return ApiResp(status_code=401)
            elif self._db._model.del_wrk(con, usr=usr, soc=check.obj):
                return ApiResp(status_code=201)
            else:
                return ApiResp(status_code=401)
