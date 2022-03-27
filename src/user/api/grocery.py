
from flask_restful import Resource
from flask import request
from bleach import clean

from user.grocerySerializer import Object, CreateAward, CreatePub, CreateSoc
from setting.decs import Auth as authenticate, Responders as response
from setting.dbcon import DbSet as __DBSET
from setting.helper import FileUp


class Awards(Resource):
    """
    User Resource
    """

    def __init__(self) -> None:
        self._db = __DBSET(sql_filename="groce.pgsql")
        self._failed_rits = "You are not qualified for this operation"
        self._unknown_req = "Unknown API request"
        self.notfnd = "Item not found in resource"

    @response
    @authenticate
    def post(self, usr, token_status):

        if isinstance(usr, tuple) and usr != 401:
            usr = usr.usr
        else:
            return usr, token_status

        awd_data = request.get_json()
        
        if not (check := CreateAward(plc=awd_data.get('plc'), act=awd_data.get('orgsatn'), titl=awd_data.get('ttl'),
            awdt=awd_data.get('dt')
        )):
            return 401

        with self._db.get_db() as con:
            self._db._model.cr8_awd(
                con, usr=usr, plc=clean(check.plc), acts=clean(check.acts), titl=clean(check.title), 
                awdt=check.awdt
            )
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
                data = self._db._model.usr_awds(con, usr=usr)
                return 201, data
            elif id := qs.get("id"): 
                data = self._db._model.awd(con, id=id)
                return 201, data
            elif srch := qs["srch"]:
                data = self._db._model.awds(con, usr=usr, pg=srch)
                return 201, data
        return 401, self._unknown_req
    
    @response
    @authenticate
    def put(self, usr, token_status):
        # get the post data

        if isinstance(usr, tuple) and usr != 401:
            usr = usr.usr
        else:
            return usr, token_status

        awd_data = request.get_json()

        if not (check := CreateAward(plc=awd_data.get('plc'), act=awd_data.get('orgsatn'), titl=awd_data.get('ttl'),
            awdt=awd_data.get('dt'), awd=awd_data.get('award')
        )):
            return 401
        with self._db.get_db() as con:
            if self._db._model.awd_rit(
                con, usr=usr, awd=check.obj
            ):
                return 401, self._failed_rits
            elif self._db._model.cr8_awd(
                con, usr=usr, plc=clean(check.plc), acts=clean(check.acts), titl=clean(check.title), 
                awdt=check.awdt
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
        
        awd = request.values

        if not (check := Object(plc=awd.get('awd'))):
            return 401
        with self._db.get_db() as con:
            if self._db._model.awd_rit(con, usr=usr, awd=check.obj):
                return 401, self._failed_rits
            elif self._db._model.del_awd(con, usr=usr, awd=check.obj):
                return 201
            else:
                return 401, self._unknown_req
    
    def options(self):
        return {'Allow' : ['POST', 'GET']}, 200, \
        {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods' : '*',
        'Access-Control-Allow-Headers': '*', 'cross-site-cookies': 'session', 
        'samesite': 'Lax'}

class Pubs(Awards):
    """get all events with get request and insert event with post request"""

    @response
    @authenticate
    def post(self, usr, token_status):

        if isinstance(usr, tuple) and usr != 401:
            usr = usr.usr
        else:
            return usr, token_status

        pub_data = request.get_json()
        
        if not (check := CreatePub(rsrch=pub_data.get('org'), dfld=pub_data.get('fld'), dttl=pub_data.get('titl'),
            fyl=pub_data.get('fyl'), pdt=pub_data.get('pdt')
        )):
            return 401

        with self._db.get_db() as con:
            self._db._model.cr8_pub(con, usr=usr, srch=check.instn, fld=clean(check.dfld), ttl=clean(check.dttl), 
                fyl=check.med, pdt=check.pdt
            )
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
                data = self._db._model.usr_pubs(con, usr=usr)
                return 201, data
            if id := qs.get("id"): 
                data = self._db._model.pub(con, usr=usr, pub=id)
                if data:
                    return 201, data
                return 404, self.notfnd
            elif pg := qs["pg"]:
                data = self._db._model.pubs(con, usr=usr, pg=pg)
                if data:
                    return 201, data
                return 404, self.notfnd
        return 401, self._unknown_req
    
    @response
    @authenticate
    def put(self, usr, token_status):
        # get the post data

        if isinstance(usr, tuple) and usr != 401:
            usr = usr.usr
        else:
            return usr, token_status

        pub_data = request.get_json()

        if not (check := CreatePub(rsrch=pub_data.get('org'), dfld=pub_data.get('fld'), dttl=pub_data.get('titl'),
            fyl=pub_data.get('fyl'), pdt=pub_data.get('pdt'), pub=pub_data.get('pub')
        )):
            return 401
        with self._db.get_db() as con:
            if self._db._model.pub_rit(con, usr=usr, awd=check.obj):
                return 401, self._failed_rits
            elif self._db._model.upd8_pub(con, usr=usr, srch=check.instn, fld=clean(check.dfld), ttl=clean(check.dttl), 
                fyl=check.med, pdt=check.pdt
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

        pub = request.values

        if not (check := Object(obj=pub.get('pub'))):
            return 401
        with self._db.get_db() as con:
            if self._db._model.pub_rit(con, usr=usr, awd=check.obj):
                return 401, self._failed_rits
            elif self._db._model.del_pub(con, usr=usr, pub=check.obj):
                return 201
            else:
                return 401, self._unknown_req

class Socs(Pubs):
    """API for all hubbies or interests outside studies"""

    @response
    @authenticate
    def post(self, usr, token_status):

        if isinstance(usr, tuple) and usr != 401:
            usr = usr.usr
        else:
            return usr, token_status

        soc_data = request.get_json()
        
        if not (check := CreateSoc(titl=soc_data.get('titl'), typ=soc_data.get('typ'))):
            return 401
        with self._db.get_db() as con:
            self._db._model.cr8_soc(con, usr=usr, typ=clean(check.typ), ttl=clean(check.title))
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
                data = self._db._model.usr_socs(con, usr=usr)
                return 201, data
            elif srch := qs["srch"]:
                data = self._db._model.socs(con, usr=usr, pg=srch)
                return 201, data
            if id := qs.get("id"): # takes user to social arena
                data = self._db._model.soc(con, usr=usr, id=id)
                return 201, data
            
        return 401, self._unknown_req

    @response
    @authenticate
    def put(self, usr, token_status):
        # get the post data

        if isinstance(usr, tuple) and usr != 401:
            usr = usr.usr
        else:
            return usr, token_status

        soc_data = request.get_json()

        if not (check := CreateSoc(titl=soc_data.get('titl'), typ=soc_data.get('typ'))):
            return 401

        with self._db.get_db() as con:
            if self._db._model.soc_rit(con, usr=usr, awd=check.obj):
                return 401, self._failed_rits
            elif self._db._model.upd8_soc(con, usr=usr, typ=clean(check.typ), ttl=clean(check.title)):
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

        soc = request.values

        if not (check := Object(obj=soc.get('soc'))):
            return 401
        with self._db.get_db() as con:
            if self._db._model.soc_rit(con, usr=usr, soc=check.obj):
                return 401, self._failed_rits
            elif self._db._model.del_soc(con, usr=usr, soc=check.obj):
                return 201
            else:
                return 401, self._unknown_req


class Avatars(Socs):
    """
    basic education or acquired skill
    """

    @response
    @authenticate
    def post(self, usr, token_status):

        if isinstance(usr, tuple) and usr != 401:
            usr = usr.usr
        else:
            return usr, token_status
        
        file = request.files
        print(request.form)
        print(request.args)

        upload = FileUp(file=file["file"])
        if not (check:= upload()):
            return 401
        print(check)
        with self._db.get_db() as con:
            self._db._model.cr8_pix(con, medfor=usr, file_path=check)
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
        else:
            usr_data = None
        
        with self._db.get_db(data_level=1) as con:
            if usr_data:
                print(usr_data)
                data = self._db._model.pix(con, usr=usr_data)
                return 201, data
            elif id := qs.get("id"): 
                data = self._db._model.pixs(con, usr=usr, id=id)
                return 201, data
        return 401, self._unknown_req

    @response
    @authenticate
    def delete(self, usr, token_status):
        """reset password"""

        if isinstance(usr, tuple) and usr != 401:
            usr = usr.usr
        else:
            return usr, token_status

        pix = request.values

        if not (check := Object(obj=pix.get('pix'))):
            return 401
        with self._db.get_db() as con:
            if self._db._model.pix_rit(con, usr=usr, pix=check.obj):
                return 401, self._failed_rits
            elif self._db._model.del_pix(con, usr=usr, pix=check.obj):
                return 201
            else:
                return 401, self._unknown_req

class Profiles(Socs):
    """
    basic education or acquired skill
    """

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
                data = self._db._model.usr_prof(con, usr=usr)
                return 201, data
            elif srch := qs["init"]:
                con = self._db.get_db()
                data = self._db._model.prof_arenz(con, usr=usr)
                return 201, data
            elif srch := qs["srch"]:
                data = self._db._model.profs(con, usr=usr, pg=srch)
                return 201, data
            elif id := qs.get("id"): 
                data = self._db._model.prof(con, usr=usr, id=id)
                return 201, data
            
        return 401, self._unknown_req