
from flask_restful import Resource
from flask import request
from bleach import clean
from pydantic import ValidationError

from user.grocerySerializer import Object, CreateAward, CreateSoc
from setting.decs import Auth as authenticate, Responders as response
from setting.dbcon import DbSet as _DBSET
from setting.helper import FileUp, convert_errors


class Awards(Resource):
    """
    User Resource
    """

    def __init__(self) -> None:
        self._db = _DBSET(sql_filename="groce.pgsql")

    @response
    @authenticate
    def post(self, usr):
        """Register user's award profile as many as user have

        Args:
            usr (int): the user from token authentication
            token_status (Bool): The status of the token, if it is time bound

        Returns:
            response_code(int): The status code of the response
            response_message(str): The response status message
        """

        if isinstance(usr, tuple):
            return usr

        awd_data = request.get_json()
        
        try:
           check = CreateAward(
               plc=awd_data.get('plc'), act=awd_data.get('orgsatn'), ttl=awd_data.get('ttl'),
                awdt=awd_data.get('awdt')
            )
        except ValidationError as err:
            errors = convert_errors(err=err)
            return 422, errors

        with self._db.get_db() as con:
            self._db._model.cr8_awd(
                con, usr=usr, plc=clean(check.plc), acts=clean(check.acts), titl=clean(check.ttl), 
                awdt=check.awdt
            )
        return 201

    @response
    @authenticate
    def get(self, usr):
        """Fetct a record of user's work profile
        Args:
            usr (int): the user from token authentication
            token_status (Bool): The status of the token, if it is time bound

        Returns:
            response_code(int): The status code of the response
            response_message(str): The response status message
        """

        if isinstance(usr, tuple):
            return usr

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
        return 401
    
    @response
    @authenticate
    def put(self, usr):
        """Update a record of user's work profile
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

        awd_data = request.get_json()
        
        try:
           check = CreateAward(
                plc=awd_data.get('plc'), act=awd_data.get('orgsatn'), ttl=awd_data.get('ttl'),
                awdt=awd_data.get('dt'), awd=awd_data.get('award')
            )
        except ValidationError as err:
            errors = convert_errors(err=err)
            return 422, errors

        with self._db.get_db() as con:
            if self._db._model.awd_rit(con, usr=usr, awd=check.obj):
                return 401
            elif self._db._model.cr8_awd(
                con, usr=usr, plc=clean(check.plc), acts=clean(check.acts), titl=clean(check.ttl), 
                awdt=check.awdt
            ):
                return 201
            else:
                return 401

    @response
    @authenticate
    def delete(self, usr):
        """Delete a record of user's work profile

        Args:
            usr (int): the user from token authentication
            token_status (Bool): The status of the token, if it is time bound

        Returns:
            response_code(int): The status code of the response
            response_message(str): The response status message
        """

        if isinstance(usr, tuple):
            return usr
        
        awd = request.values

        if not (check := Object(plc=awd.get('awd'))):
            return 401
        with self._db.get_db() as con:
            if self._db._model.awd_rit(con, usr=usr, awd=check.obj):
                return 401
            elif self._db._model.del_awd(con, usr=usr, awd=check.obj):
                return 201
            else:
                return 401
    
    def options(self):
        return {'Allow' : ['POST', 'GET']}, 200, \
        {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods' : '*',
        'Access-Control-Allow-Headers': '*', 'cross-site-cookies': 'session', 
        'samesite': 'Lax'}


class Socs(Awards):
    """API for all hubbies or interests outside studies"""

    @response
    @authenticate
    def post(self, usr):
        """Register user's hubby profile
        Args:
            usr (int): the user from token authentication
            token_status (Bool): The status of the token, if it is time bound

        Returns:
            response_code(int): The status code of the response
            response_message(str): The response status message
        """

        if isinstance(usr, tuple):
            return usr

        soc_data = request.get_json()
        
        try:
           check = CreateSoc(titl=soc_data.get('titl'), typ=soc_data.get('typ'))
        except ValidationError as err:
            errors = convert_errors(err=err)
            return 422, errors

        with self._db.get_db() as con:
            self._db._model.cr8_soc(con, usr=usr, typ=clean(check.typ), ttl=clean(check.title))
        return 201

    @response
    @authenticate
    def get(self, usr):
        """Fetch a user's hubby profile
    
        Args:
            usr (int): the user from token authentication
            token_status (Bool): The status of the token, if it is time bound

        Returns:
            response_code(int): The status code of the response
            response_message(str): The response status message
        """

        if isinstance(usr, tuple):
            return usr

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
            
        return 401

    @response
    @authenticate
    def put(self, usr):
        """Update a user's hubby profile

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

        soc_data = request.get_json()
        
        try:
           check = CreateSoc(titl=soc_data.get('titl'), typ=soc_data.get('typ'))
        except ValidationError as err:
            errors = convert_errors(err=err)
            return 422, errors

        with self._db.get_db() as con:
            if self._db._model.soc_rit(con, usr=usr, awd=check.obj):
                return 401
            elif self._db._model.upd8_soc(con, usr=usr, typ=clean(check.typ), ttl=clean(check.title)):
                return 201
            else:
                return 401

    @response
    @authenticate
    def delete(self, usr):
        """Delete a user's hubby profile

        Args:
            usr (int): the user from token authentication
            token_status (Bool): The status of the token, if it is time bound

        Returns:
            response_code(int): The status code of the response
            response_message(str): The response status message
        """

        if isinstance(usr, tuple):
            return usr

        soc = request.values

        if not (check := Object(obj=soc.get('soc'))):
            return 401
        with self._db.get_db() as con:
            if self._db._model.soc_rit(con, usr=usr, soc=check.obj):
                return 401
            elif self._db._model.del_soc(con, usr=usr, soc=check.obj):
                return 201
            else:
                return 401


class Avatars(Socs):
    """
    basic education or acquired skill
    """

    @response
    @authenticate
    def post(self, usr):
        """Upload a user's profile picture

        Args:
            usr (int): the user from token authentication
            token_status (Bool): The status of the token, if it is time bound

        Returns:
            response_code(int): The status code of the response
            response_message(str): The response status message
        """

        if isinstance(usr, tuple):
            return usr
        
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
    def get(self, usr):
        """Fetch a user's profile picture

        Args:
            usr (int): the user from token authentication
            token_status (Bool): The status of the token, if it is time bound

        Returns:
            response_code(int): The status code of the response
            response_message(str): The response status message
        """

        if isinstance(usr, tuple):
            return usr

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
        return 401

    @response
    @authenticate
    def delete(self, usr):
        """Delete a user's profile picture

        Args:
            usr (int): the user from token authentication
            token_status (Bool): The status of the token, if it is time bound

        Returns:
            response_code(int): The status code of the response
            response_message(str): The response status message
        """

        if isinstance(usr, tuple):
            return usr

        pix = request.values

        if not (check := Object(obj=pix.get('pix'))):
            return 401
        with self._db.get_db() as con:
            if self._db._model.pix_rit(con, usr=usr, pix=check.obj):
                return 401
            elif self._db._model.del_pix(con, usr=usr, pix=check.obj):
                return 201
            else:
                return 401

class Profiles(Socs):
    """
    basic education or acquired skill
    """

    @response
    @authenticate
    def get(self, usr):
        """_summary_

        Args:
            usr (int): the user from token authentication
            token_status (Bool): The status of the token, if it is time bound

        Returns:
            response_code(int): The status code of the response
            response_message(str): The response status message
        """

        if isinstance(usr, tuple):
            return usr

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
        return 401
    