
from flask_restful import Resource
from flask import request
from bleach import clean

from profile.profSerializer import Object, Basics, Resrch, Place, Acads
from setting.decs import Auth as authenticate, Responders as response
from setting.dbcon import DbSet


class Basic(Resource):
    """
    basic education or acquired skill
    """

    def __init__(self):
        self._db = DbSet(sql_filename="prof.pgsql")
        self._failed_rits = "You are not qualified for this operation"
        self._unknown_req = "Unknown API request"

    @response
    @authenticate
    def post(self, usr, token_status):
        # get the post data

        if isinstance(usr, tuple) and usr.usr != 401:
            usr = usr.usr
        else:
            return usr, token_status
        
        bsic_data = request.get_json()

        if not (check:= Basics(dspln=bsic_data.get('dspln'), place=bsic_data.get('plc'), strtd=bsic_data.get('strt'), 
                endd=bsic_data.get('end'),  acad=bsic_data.get('typ')
            )):
            return 401
        
        with self._db.get_db() as con:
            self._db._model.cr8_base(con, usr=usr, dspln=clean(check.dspln), plc=clean(check.place), 
                strtd=check.strtd, endd=check.endd, typ=check.acad
            )
            return 201

    @response
    @authenticate
    def get(self, usr, token_status):

        if isinstance(usr, tuple) and usr.usr != 401:
            usr = usr.usr
        else:
            return usr, token_status

        if not (qs := request.values):
            usr_data = usr

        with self._db.get_db(data_level=1) as con:
            if usr_data:
                data = self._db._model.usr_base(con, usr=usr)
                return 201, data
            if id := qs.get("id"): 
                data = self._db._model.base(con, usr=usr, id=id)
                return 201, data
            elif srch := qs.get("srch"): # this goes with search
                data = self._db._model.bases(con, usr=usr, pg=srch)
                return 201, data
        return 401, self._unknown_req

    @response
    @authenticate
    def put(self, usr, token_status):
        # get the post data

        if isinstance(usr, tuple) and usr.usr != 401:
            usr = usr.usr
        else:
            return usr, token_status

        bsic_data = request.get_json()

        if not (check := Basics(dspln=bsic_data.get('displn'), place=bsic_data.get('plc'), strtd=bsic_data.get('strt'), 
                endd=bsic_data.get('end'),  acad=bsic_data.get('typ')
            )):
            return 401
        with self._db.get_db() as con:
            if not self._db._model.base_rit(con, usr=usr, base=check.obj):
                return 401, self._failed_rits
            if self._db._model.upd8_base(con, usr=usr, dspln=clean(check.dspln), plc=clean(check.place), 
                strtd=check.strtd, endd=check.endd, typ=check.acad
            ):
                return 201
            else:
                return 401, self._unknown_req

    @response
    @authenticate
    def delete(self, usr, token_status):
        """reset password"""

        if isinstance(usr, tuple) and usr != 401:
            usr = usr.usr
        else:
            return usr, token_status
        
        base = request.values

        if not (check := Object(obj=base.get('soc'))):
            return 401
        with self._db.get_db() as con:
            if self._db._model.base_rit(con, usr=usr, soc=check.obj):
                return 401, self._failed_rits
            elif self._db._model.del_base(con, usr=usr, soc=check.obj):
                return 201
            else:
                return 401, self._unknown_req

    def options(self):
        return {'Allow' : ['POST', 'GET']}, 200, \
        {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods' : '*',
        'Access-Control-Allow-Headers': '*', 'cross-site-cookies': 'session', 
        'samesite': 'Lax'}

class Accademics(Basic):
    """
    User Login Resource
    """

    @response
    @authenticate
    def post(self, usr, token_status):

        if isinstance(usr, tuple) and usr.usr != 401:
            usr = usr.usr
        else:
            return usr, token_status
        
        acad_data = request.get_json()

        if not (check := Acads(
                dspln=acad_data.get('displn'), place=acad_data.get('plc'),
                ttl=acad_data.get('ttl'), strtd=acad_data.get('strt'), endd=acad_data.get('end')
            )):
            return 401

        with self._db.get_db() as con:
            if not (base:= self._db._model.acadqfn(con, usr=usr)):
                print(usr, token_status)
                print(base)
                return 401, self._failed_rits
            self._db._model.cr8_acad(
                con, usr=usr, dspln=clean(check.dspln), plc=clean(check.place),  
                base=base, stg=clean(check.ttl), strtd=check.strtd, endd=check.endd,
            )
            return 201

    @response
    @authenticate
    def get(self, usr, token_status):
        """get accademics data"""

        if isinstance(usr, tuple) and usr.usr != 401:
            usr = usr.usr
        else:
            return usr, token_status
        
        if not (qs := request.values):
            usr_data = usr
        
        with self._db.get_db(data_level=1) as con:
            if usr_data:
                data = self._db._model.usr_acada(con, usr=usr)
                return 201, data
            if id := qs.get("id"): 
                data = self._db._model.acada(con, usr=usr, id=id)
                return 201, data
            elif srch := qs.get("srch"):
                data = self._db._model.acadas(con, usr=usr, pg=srch)
                return 201, data
            return 401, self._unknown_req

    @response
    @authenticate
    def put(self, usr, token_status):
        # get the post data

        if isinstance(usr, tuple) and usr.usr != 401:
            usr = usr.usr
        else:
            return usr, token_status

        acad_data = request.get_json()
        
        if not (check := Acads(
                dspln=acad_data.get('dspln'), place=acad_data.get('plc'),
                ttl=acad_data.get('ttl'), strtd=acad_data.get('strt'), endd=acad_data.get('end')
            )):
            return 401
        with self._db.get_db() as con:
            if not self._db._model.upd8_acad(
                con, usr=usr, dspln=clean(check.dspln), plc=clean(check.place),  
                stg=clean(check.ttl), strtd=check.strtd, endd=check.endd,
            ):
                return 201
            else:
                return 401, self._unknown_req

    @response
    @authenticate
    def delete(self, usr, token_status):
        """reset password"""

        if isinstance(usr, tuple) and usr.usr != 401:
            usr = usr.usr
        else:
            return usr, token_status

        acad = request.values
        
        if not (check := Object(obj=acad.get('acad'))):
            return 401
        with self._db.get_db() as con:
            if not self._db._model.acad_rit(con, usr=usr, soc=check.obj):
                return 401
            elif self._db._model.del_acad(con, usr=usr, soc=check.obj):
                return 201
            else:
                return 401, self._unknown_req

class Resacher(Accademics):
    """
    Logout Resource
    """
    
    @response
    @authenticate
    def post(self, usr, token_status):
        if isinstance(usr, tuple) and usr != 401:
            usr = usr.usr
        else:
            return usr, token_status
        
        rsrcha = request.get_json()
        if not (check := Resrch(dspln=rsrcha.get('displn'), place=rsrcha.get('plc'), typ=rsrcha.get('typ'),
            emel=rsrcha.get('emel'), strtd=rsrcha.get('strt'), endd=rsrcha.get('end'))):
            return
        with self._db.get_db() as con:
            if not (acad := self._db._model.rsrchaqfn(con, usr=usr)):
                return 401, self._failed_rits
            self._db._model.cr8_srcha(con, usr=usr, cnt=check.emel, base=acad, org=check.place, 
            dspln=check.dspln, typ=check.typ, strtd=check.strtd, endd=check.endd)
        return 201

    @response
    @authenticate
    def get(self, usr, token_status):
        """reset password"""

        if isinstance(usr, tuple) and usr != 401:
            usr = usr.usr
        else:
            return usr, token_status

        if not (qs := request.values):
            usr_data = usr
        
        with self._db.get_db(data_level=1) as con:
            if usr_data:
                data = self._db._model.rsrcha(con, usr=usr)
                return 201, data
            elif id := qs.get("id"): 
                data = self._db._model.srcha(con, usr=usr, id=id)
                return 201, data
            elif srch := qs["srch"]:
                data = self._db._model.srchas(con, usr=usr, pg=srch)
                return 201, data
            return 401, self._unknown_req

    @response    
    @authenticate
    def put(self, usr, token_status):
        # get the post data

        if isinstance(usr, tuple) and usr.usr != 401:
            usr = usr.usr
        else:
            return usr, token_status

        rsrch_data = request.get_json()

        if not (check := Resrch(
                typ=rsrch_data.get('typ'), place=rsrch_data.get('plc'), dspln=rsrch_data.get('displn'), 
                email=rsrch_data.get('emel'), strtd=rsrch_data.get('strt'), endd=rsrch_data.get('end')
            )):
            return 401
        with self._db.get_db() as con:
            if not self._db._model.upd8_srcha(
                con, usr=usr, cnt=check.email, org=clean(check.place), dspln=clean(check.dspln), 
                typ=check.typ, strtd=check.strtd, endd=check.endd
            ):
                return 201
            else:
                return 401, self._unknown_req

    @response
    @authenticate
    def delete(self, usr, token_status):
        """reset password"""

        if isinstance(usr, tuple) and usr.usr != 401:
            usr = usr.usr
        else:
            return usr, token_status

        srcha = request.values
        
        if not (check := Object(obj=srcha.get('srcha'))):
            return 401
        with self._db.get_db() as con:
            if self._db._model.srcha_rit(con, usr=usr, soc=check.obj):
                return 401
            elif self._db._model.del_srcha(con, usr=usr, soc=check.obj):
                return 201
            else:
                return 401, self._unknown_req

class Works(Resacher):
    """
    basic education or acquired skill
    """

    @response
    @authenticate
    def post(self, usr, token_status):
        # get the post data

        if isinstance(usr, tuple) and usr.usr != 401:
            usr = usr.usr
        else:
            return usr, token_status

        wrk_data = request.get_json()

        if not (check:= Place(
                    dspln=wrk_data.get('dspln'), place=wrk_data.get('plc'),
                    strtd=wrk_data.get('strt'), endd=wrk_data.get('end')
                )):
            return 401

        with self._db.get_db() as con:
            self._db._model.cr8_wrk(
                con, usr=usr, plc=clean(check.place), dng=clean(check.dspln), strtd=check.strtd, endd=check.endd
            )
        return 201

    @response
    @authenticate
    def get(self, usr, token_status):
        """reset password"""

        if isinstance(usr, tuple) and usr.usr != 401:
            usr = usr.usr
        else:
            return usr, token_status
        
        if not (qs := request.values):
            usr_data = usr
        else:
            usr_data = None
        
        with self._db.get_db(data_level=1) as con:
            if usr_data:
                data = self._db._model.usr_wrk(con, usr=usr)
                return 201, data
            elif id := qs.get("id"): 
                data = self._db._model.wrk(con, usr=usr, id=id)
                return 201, data
            elif srch := qs["srch"]:
                data = self._db._model.wrks(con, usr=usr, pg=srch)
                return 201, data
        return 401, self._unknown_req

    @response
    @authenticate
    def put(self, usr, token_status):
        # get the post data

        if isinstance(usr, tuple) and usr.usr != 401:
            usr = usr.usr
        else:
            return usr, token_status

        wrk_data = request.get_json()

        if not (check := Place(dspln=wrk_data.get('displn'), place=wrk_data.get('plc'),
                strtd=wrk_data.get('strt'), endd=wrk_data.get('end')
            )):
            return 401
        with self._db.get_db() as con:
            if not self._db._model.upd8_wrk(
                con, usr=usr, plc=clean(check.place), dng=clean(check.dspln), strtd=check.strtd, endd=check.endd
            ):
                return 201
            else:
                return 401, self._unknown_req

    @response
    @authenticate
    def delete(self, usr, token_status):
        """reset password"""

        if isinstance(usr, tuple) and usr.usr != 401:
            usr = usr.usr
        else:
            return usr, token_status

        wrk = request.values
        
        if not (check := Object(obj=wrk.get('wrk'))):
            return 401
        with self._db.get_db() as con:
            if self._db._model.wrk_rit(con, usr=usr, soc=check.obj):
                return 401, self._failed_rits
            elif self._db._model.del_wrk(con, usr=usr, soc=check.obj):
                return 201
            else:
                return 401, self._unknown_req
