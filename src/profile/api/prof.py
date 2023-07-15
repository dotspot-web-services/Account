
from flask_restful import Resource
from pydantic import ValidationError
from flask import request
from bleach import clean

from profile.profSerializer import Object, Basics, Resrch, Place, Acads
from setting.decs import Auth as authenticate, Responders as response
from setting.dbcon import DbSet
from setting.helper import convert_errors


class Basic(Resource):
    """
    basic education or acquired skill
    """

    def __init__(self):
        self._db = DbSet(sql_filename="prof.pgsql")


    @response
    @authenticate
    def post(self, usr):
        """Register user's basic accademic or skill profile

        Args:
            usr (int): the user from token authentication
            token_status (Bool): The status of the token, if it is time bound

        Returns:
            response_code(int): The status code of the response
            response_message(str): The response status message
        """
        # get the post data
        if isinstance(usr, tuple):
            return usr
        
        bsic_data = request.get_json()
        try:
           check = Basics(fld=bsic_data.get('fld'), locatn=bsic_data.get('locatn'), strt=bsic_data.get('strt'), 
                end=bsic_data.get('end'),  acad=bsic_data.get('acad')
            )
        except ValidationError as err:
            errors = convert_errors(err=err)
            return 422, errors
        
        with self._db.get_db() as con:
            self._db._model.cr8_base(con, usr=usr, dspln=clean(check.fld), plc=clean(check.locatn), 
                strtd=check.strt, endd=check.end, typ=check.acad
            )
            return 201

    @response
    @authenticate
    def get(self, usr):
        """Fetch user's basic accademic or skill profile

        Args:
            usr (int): the user from token authentication
            token_status (Bool): The status of the token, if it is time bound

        Returns:
            response_code(int): The status code of the response
            response_message(str): The response status message
        """

        if isinstance(usr, tuple):
            return usr

        with self._db.get_db(data_level=1) as con:
            
            if id := request.values.get("id"): 
                data = self._db._model.base(con, usr=usr, id=id)
                return 200, data
            elif usr:
                data = self._db._model.usr_base(con, usr=usr)
                return 200, data
            #elif srch := qs.get("srch"): # this goes with search
            #    data = self._db._model.bases(con, usr=usr, pg=srch)
            #    return 201, data
        return 404

    @response
    @authenticate
    def put(self, usr):
        """Update user's basic accademic or skill profile

        Args:
            usr (int): the user from token authentication
            token_status (Bool): The status of the token, if it is time bound

        Returns:
            response_code(int): The status code of the response
            response_message(str): The response status message
        """
        # get the post data
        if isinstance(usr, tuple):
            return usr
        bsic_data = request.get_json()
        
        try:
           check = Basics(fld=bsic_data.get('fld'), locatn=bsic_data.get('locatn'), strt=bsic_data.get('strt'), 
                end=bsic_data.get('end'),  acad=bsic_data.get('acad')
            )
        except ValidationError as err:
            errors = convert_errors(err=err)
            return 422, errors

        with self._db.get_db() as con:
            if not self._db._model.base_rit(con, usr=usr, base=check.obj):
                return 401, self._failed_rits
            if self._db._model.upd8_base(con, usr=usr, dspln=clean(check.fld), plc=clean(check.locatn), 
                strtd=check.strt, endd=check.end, typ=check.acad
            ):
                return 201
            else:
                return 404

    @response
    @authenticate
    def delete(self, usr):
        """Delete user's basic accademic or skill profile

        Args:
            usr (int): the user from token authentication
            token_status (Bool): The status of the token, if it is time bound

        Returns:
            response_code(int): The status code of the response
            response_message(str): The response status message
        """
        
        if isinstance(usr, tuple):
            return usr
        base = request.values

        if not (check := Object(obj=base.get('soc'))):
            return 401
        with self._db.get_db() as con:
            if self._db._model.base_rit(con, usr=usr, soc=check.obj):
                return 401, self._failed_rits
            elif self._db._model.del_base(con, usr=usr, soc=check.obj):
                return 201
            else:
                return 404

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
    def post(self, usr):
        """Register user's basic universal accademic profile
        Check the user's basic accademic profile if qualified

        Args:
            usr (int): the user from token authentication
            token_status (Bool): The status of the token, if it is time bound

        Returns:
            response_code(int): The status code of the response
            response_message(str): The response status message
        """
        
        if isinstance(usr, tuple):
            return usr
        acad_data = request.get_json()
        
        try:
           check = Acads(
                fld=acad_data.get('fld'), loctn=acad_data.get('locatn'),
                ttl=acad_data.get('ttl'), strt=acad_data.get('strt'), end=acad_data.get('end')
            )
        except ValidationError as err:
            errors = convert_errors(err=err)
            return 422, errors

        with self._db.get_db() as con:
            if not (base:= self._db._model.acadqfn(con, usr=usr)):
                return 401, self._failed_rits
            self._db._model.cr8_acad(
                con, usr=usr, dspln=clean(check.fld), plc=clean(check.locatn),  
                base=base, stg=clean(check.ttl), strtd=check.strt, endd=check.end,
            )
            return 201

    @response
    @authenticate
    def get(self, usr):
        """Fetch user's universal accademic profile

        Args:
            usr (int): the user from token authentication
            token_status (Bool): The status of the token, if it is time bound

        Returns:
            response_code(int): The status code of the response
            response_message(str): The response status message
        """
        
        if isinstance(usr, tuple):
            return usr
        
        with self._db.get_db(data_level=1) as con:
            
            if id := request.values.get("id"): 
                data = self._db._model.acada(con, usr=usr, id=id)
                return 201, data
            elif usr:
                data = self._db._model.usr_acada(con, usr=usr)
                return 201, data
            #elif srch := qs.get("srch"):
            #    data = self._db._model.acadas(con, usr=usr, pg=srch)
            #    return 201, data
            return 404

    @response
    @authenticate
    def put(self, usr):
        """Update user's basic universal accademic profile if existing record

        Args:
            usr (int): the user from token authentication
            token_status (Bool): The status of the token, if it is time bound

        Returns:
            response_code(int): The status code of the response
            response_message(str): The response status message
        """
        # get the post data

        if isinstance(usr, tuple):
            return usr
        acad_data = request.get_json()
        
        try:
           check = Acads(
                fld=acad_data.get('fld'), locatn=acad_data.get('locatn'),
                ttl=acad_data.get('ttl'), strt=acad_data.get('strt'), end=acad_data.get('end')
            )
        except ValidationError as err:
            errors = convert_errors(err=err)
            return 422, errors
        
        with self._db.get_db() as con:
            if not self._db._model.upd8_acad(
                con, usr=usr, dspln=clean(check.fld), plc=clean(check.locatn),  
                stg=clean(check.ttl), strtd=check.strt, endd=check.end,
            ):
                return 201
            else:
                return 404
    @response
    @authenticate
    def delete(self, usr):
        """Delete user's basic universal accademic profile

        Args:
            usr (int): the user from token authentication
            token_status (Bool): The status of the token, if it is time bound

        Returns:
            response_code(int): The status code of the response
            response_message(str): The response status message
        """

        if isinstance(usr, tuple):
            return usr
        acad = request.values
        
        if not (check := Object(obj=acad.get('acad'))):
            return 401
        with self._db.get_db() as con:
            if not self._db._model.acad_rit(con, usr=usr, soc=check.obj):
                return 401
            elif self._db._model.del_acad(con, usr=usr, soc=check.obj):
                return 201
            else:
                return 404

class Resacher(Accademics):
    """
    Logout Resource
    """
    
    @response
    @authenticate
    def post(self, usr):
        """Register user's Research profile as an accademic

        Args:
            usr (int): the user from token authentication
            token_status (Bool): The status of the token, if it is time bound

        Returns:
            response_code(int): The status code of the response
            response_message(str): The response status message
        """
        
        if isinstance(usr, tuple):
            return usr
        rsrcha = request.get_json()
        
        try:
           check = Resrch(
                fld=rsrcha.get('fld'), locatn=rsrcha.get('locatn'), typ=rsrcha.get('typ'),
                emel=rsrcha.get('emel'), strt=rsrcha.get('strt'), end=rsrcha.get('end')
            )
        except ValidationError as err:
            errors = convert_errors(err=err)
            return 422, errors
        
        with self._db.get_db() as con:
            if not (acad := self._db._model.rsrchaqfn(con, usr=usr)):
                return 401, self._failed_rits
            self._db._model.cr8_srcha(con, usr=usr, cnt=check.emel, base=acad, org=check.locatn, 
            dspln=check.fld, typ=check.typ, strtd=check.strt, endd=check.end)
        return 201

    @response
    @authenticate
    def get(self, usr):
        """Fetch user's Research profile as an accademic

        Args:
            usr (int): the user from token authentication
            token_status (Bool): The status of the token, if it is time bound

        Returns:
            response_code(int): The status code of the response
            response_message(str): The response status message
        """

        if isinstance(usr, tuple):
            return usr
        
        with self._db.get_db(data_level=1) as con:
            if id := request.values.get("id"): 
                data = self._db._model.srcha(con, usr=usr, id=id)
                return 201, data
            elif usr:
                data = self._db._model.rsrcha(con, usr=usr)
                return 201, data
            #elif srch := qs["srch"]:
            #    data = self._db._model.srchas(con, usr=usr, pg=srch)
            #    return 201, data
            return 404

    @response    
    @authenticate
    def put(self, usr):
        """Update user's Research profile as an accademic if existing profile
        Args:
            usr (int): the user from token authentication
            token_status (Bool): The status of the token, if it is time bound

        Returns:
            response_code(int): The status code of the response
            response_message(str): The response status message
        """
        # get the post data

        if isinstance(usr, tuple):
            return usr
        rsrcha = request.get_json()
        
        try:
           check = Resrch(
                 fld=rsrcha.get('fld'), locatn=rsrcha.get('locatn'), typ=rsrcha.get('typ'),
                emel=rsrcha.get('emel'), strt=rsrcha.get('strt'), end=rsrcha.get('end')
            )
        except ValidationError as err:
            errors = convert_errors(err=err)
            return 422, errors

        with self._db.get_db() as con:
            if not self._db._model.upd8_srcha(
                con, usr=usr, cnt=check.emel, org=clean(check.locatn), dspln=clean(check.fld), 
                typ=check.typ, strtd=check.strt, endd=check.end
            ):
                return 201
            else:
                return 404

    @response
    @authenticate
    def delete(self, usr):
        """Delete user's Research profile as an accademic

        Args:
            usr (int): the user from token authentication
            token_status (Bool): The status of the token, if it is time bound

        Returns:
            response_code(int): The status code of the response
            response_message(str): The response status message
        """

        if isinstance(usr, tuple):
            return usr
        srcha = request.values
        
        if not (check := Object(obj=srcha.get('srcha'))):
            return 401
        with self._db.get_db() as con:
            if self._db._model.srcha_rit(con, usr=usr, soc=check.obj):
                return 401
            elif self._db._model.del_srcha(con, usr=usr, soc=check.obj):
                return 201
            else:
                return 404

class Works(Resacher):
    """
    basic education or acquired skill
    """

    @response
    @authenticate
    def post(self, usr):
        """Register user's work profile
        Args:
            usr (int): the user from token authentication
            token_status (Bool): The status of the token, if it is time bound

        Returns:
            response_code(int): The status code of the response
            response_message(str): The response status message
        """
        # get the post data

        if isinstance(usr, tuple):
            return usr
        wrk_data = request.get_json()
        
        try:
           check = Place(
               fld=wrk_data.get('fld'), locatn=wrk_data.get('locatn'), strt=wrk_data.get('strt'), end=wrk_data.get('end')
            )
        except ValidationError as err:
            errors = convert_errors(err=err)
            return 422, errors

        with self._db.get_db() as con:
            self._db._model.cr8_wrk(
                con, usr=usr, plc=clean(check.locatn), dng=clean(check.fld), strtd=check.strt, endd=check.end
            )
        return 201

    @response
    @authenticate
    def get(self, usr):
        """Fetch user's work profile

        Args:
            usr (int): the user from token authentication
            token_status (Bool): The status of the token, if it is time bound

        Returns:
            response_code(int): The status code of the response
            response_message(str): The response status message
        """

        if isinstance(usr, tuple):
            return usr
        
        with self._db.get_db(data_level=1) as con:
            if id := request.values.get("id"): 
                data = self._db._model.wrk(con, usr=usr, id=id)
                return 201, data
            if usr:
                data = self._db._model.usr_wrk(con, usr=usr)
                return 201, data
            #elif srch := qs["srch"]:
            #    data = self._db._model.wrks(con, usr=usr, pg=srch)
            #    return 201, data
        return 404

    @response
    @authenticate
    def put(self, usr):
        """Update user's work profile if existing record

        Args:
            usr (int): the user from token authentication
            token_status (Bool): The status of the token, if it is time bound

        Returns:
            response_code(int): The status code of the response
            response_message(str): The response status message
        """
        # get the post data

        if isinstance(usr, tuple):
            return usr
        wrk_data = request.get_json()
        
        try:
           check = Place(
               fld=wrk_data.get('fld'), locatn=wrk_data.get('locatn'), strt=wrk_data.get('strt'), end=wrk_data.get('end')
            )
        except ValidationError as err:
            errors = convert_errors(err=err)
            return 422, errors

        with self._db.get_db() as con:
            if not self._db._model.upd8_wrk(
                con, usr=usr, plc=clean(check.locatn), dng=clean(check.fld), strtd=check.strt, endd=check.end
            ):
                return 201
            else:
                return 401

    @response
    @authenticate
    def delete(self, usr):
        """Delete user's work profile

        Args:
            usr (int): the user from token authentication
            token_status (Bool): The status of the token, if it is time bound

        Returns:
            response_code(int): The status code of the response
            response_message(str): The response status message
        """

        if isinstance(usr, tuple):
            return usr        
        wrk = request.values
        
        if not (check := Object(obj=wrk.get('wrk'))):
            return 401
        with self._db.get_db() as con:
            if self._db._model.wrk_rit(con, usr=usr, soc=check.obj):
                return 401, self._failed_rits
            elif self._db._model.del_wrk(con, usr=usr, soc=check.obj):
                return 201
            else:
                return 404
