
import bcrypt

from flask import request
from flask_restful import Resource
from bleach import clean
from pydantic import ValidationError

from ..serializer import RegCheck, LogCheck, finalCheck, PwdCheck, Mailer
from setting.decs import Auth as authenticate, Responders as response
from setting.dbcon import DbSet as _DBSET
from setting.helper import convert_errors
from ..msg import SendMsg as _messenger


class Register(Resource):
    """
    User Registration Resource
    """
    
    def __init__(self):
        self._db = _DBSET()

    def __hash_pwd(self, pwd):
        """User password encryption

        Args:
            pwd (str): User's provided password

        Returns:
            str: Hashed password
        """
        return bcrypt.hashpw(
            bytes(pwd, encoding='utf-8'), bcrypt.gensalt(self._db._oda.log_rod)
        )

    @response
    def post(self):
        """A new user registeration

        Returns:
           status(int): The status of the registeration request sent
        """

        reg_data = request.form or request.get_json()

        try:
           check = RegCheck(
                fname=reg_data.get('fname'), cont=reg_data.get('cont'), pwd=reg_data.get('pwd'), vpwd=reg_data.get('vpwd')
            )
        except ValidationError as err:
            errors = convert_errors(err=err)
            return 422, errors
        #if check.cnt == check.EmailStr:
        #    cntyp = False
        #    print(check.EmailStr)
        #elif check.cnt == check.phone:
        #    cntyp = True
        #    print(check.phone)

        with self._db.get_db(data_level=2) as con:
            if self._db._model.check_acc(con, contact=check.cont):     
                return 409
            if usr := self._db._model.cr8_acc(
                con, fname=clean(check.fullname), pwd=self.__hash_pwd(pwd=check.pwd).decode('utf8'), 
                cnt=check.cnt
            ):
                token = authenticate(func=usr).encode_auth(days=1)
                return 201, token

    @response
    @authenticate
    def put(self, usr):
        """Complete preprofile data

        Args:
            usr (int): the user from token authentication
            token_status (Bool): The status of the token, if it can expire

        Returns:
            response_code(int): The status code of the response
            response_message(str): The response status message
        """

        if isinstance(usr, tuple):
            return usr
        reg_data = request.get_json()
        
        try:
           check = finalCheck(
                fname=reg_data.get('fname'), cont=reg_data.get('cont'), dob=reg_data.get('dob'),
                cntyp=reg_data.get('typ'), sx=reg_data.get('sx')
            )
        except ValidationError as err:
            errors = convert_errors(err=err)
            return 422, errors

        with self._db.get_db() as con:
            if not self._db._model.upd8_acc(
                con, usr=usr, fname=clean(check.fullname), cnt=check.cnt, emel=check.cntyp,
                bday=check.dob, mel=check.sex, actv=True, verfd= True
            ):
                return 201
            else:
                return 401
            
    @response
    def get(self):
        """Fetch users registeration data

        Returns:
            response_code(int): The status code of the response
            response_message(str): The response status message
        """

        qs = request.values
        contact = qs["contact"]

        with self._db.get_db() as con:
            if cont := self._db._model.get_cont(
                con, cnt=contact
            ):
                return 201, cont
            elif not cont:
                return 404, "Not found in resource"
        return 401

    def options(self):
        return {'Allow' : ['POST', 'PUT', 'GET']}, 200, \
        {
            'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods' : '*',
            'Access-Control-Allow-Headers': '*'
        }

class Login(Register):
    """
    User Login Resource
    """

    @response
    def post(self):
        """
        Check user account status
        Check password
        Generate a token

        Returns:
            response_code(int): The status code of the response
            response_message or token(str): The response status message or user token
        """
        # get the post data
    
        if not (auth := request.authorization or request.form):
            return 401
        (contact := auth.get("cont") or auth.username)
        (password := auth.get("pwd") or auth.password)
        
        try:
            check = LogCheck(cont=contact, pwd=password)
        except ValidationError as err:
            errors = convert_errors(err=err)
            return 422, errors

        with self._db.get_db(data_level=2) as con:
            if (usr := self._db._model.check_acc(con, contact=check.cont)) and usr is None or not usr:
               return 404
            if bcrypt.checkpw(password=check.pwd.encode('utf-8'), hashed_password=usr.pwd.encode('utf-8')):   
                if(usr_data := self._db._model.usr_status(con, contact=check.cont)) and usr_data.token == '':
                    token = authenticate(func=usr.usr).encode_auth(days=3)
                    self._db._model.cr8_tkn(con, tkn=token)
                    return 200, {"token": str(token)}
                print(usr_data)
                if usr_data.user_status is False:
                    return 401, "Account is not activated yet"
                return 201, usr_data.token
        return 401

    @response
    @authenticate
    def put(self, usr):
        """
        Check if the account request token is expired
        Udate the password and login the person
        Args:
            usr (int): the user from token authentication
            token_status (Bool): The status of the token, if it is time bound

        Returns:
            response_code(int): The status code of the response
            response_message(str): The response status message
        """
        
        #if token_status:
        #    redirect(url_for('accs.regs.finalize'))
        if isinstance(usr, tuple):
            return usr
        reg_data = request.get_json()
        
        try:
           check = PwdCheck(cont=reg_data.get('cont'),
                pwd=reg_data.get('pwd'), vpwd=reg_data.get('vpwd')
            )
        except ValidationError as err:
            errors = convert_errors(err=err)
            return 422, errors

        with self._db.get_db() as con:
            if not self._db._model.upd8_pwd(
                con, usr=usr, pwd=self.__hash_pwd(pwd=check.pwd).decode('utf8')
            ):
                return 201
            else:
                return 401
            
    @response
    def get(self):
        """Check if a user already exists through the contact

        Returns:
            response_code(int): The status code of the response
            response_message(str): The response status message
        """

        contact = request.form["cont"]

        with self._db.get_db() as con:
            if cont := self._db._model.get_cont(
                con, cnt=contact
            ):
                return 201, cont
            elif not cont:
                return 404
        return 401

class Logout(Resource):
    """
    Logout Resource
    """
    def __init__(self):
        self._db = _DBSET()

    @response
    @authenticate
    def post(self, usr):
        """
        Blacklist token 

        Args:
            usr (_type_): _description_
            token_status (_type_): _description_

        Returns:
            _type_: _description_
        """
        # get auth token
        #if isinstance(usr, tuple) and usr.usr != 401:
        #    usr = usr.usr
        
        auth_header = request.headers.get('Authorization')

        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            check_token = authenticate(func=auth_token).decode_auth()
            if not isinstance(check_token, str):
                with self._db.get_db() as con:
                    self._db._model.in_tkn(con, tkn=auth_token, usr=usr)
                    return 201
            else:
                return 401
        else:
            return 403
        
    @response
    def get(self, usr):
        """Refresh access token if expired

        Args:
            usr (_type_): _description_

        Returns:
            _type_: _description_
        """

        with self._db.get_db(data_level=1) as con:
            if data := self._db._model.usr_reg(
                con, usr=usr
            ):
                return 201, data
            else:
                return 401

    def options(self):
        return {'Allow' : ['POST', 'GET']}, 200, \
        {
            'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods' : '*',
            'Access-Control-Allow-Headers': '*'
        }


class Reset(Logout):
    """
    Logout Resource
    """
    def __init__(self):
        self._db = _DBSET()

    @response
    def post(self):
        
        """Check if a user already exists through the contact

        Returns:
            response_code(int): The status code of the response
            response_message(str): The response status message
        """

        contact = request.form["cont"]

        with self._db.get_db() as con:
            if cont := self._db._model.get_cont(con, cnt=contact) and (chanel := self._db.get_redis(db=3)):
                chanel.xadd(name="reset", fields={"contact":cont})
                return 200
        return 404
        
    @response
    def get(self, usr):
        """Refresh access token if expired

        Args:
            usr (_type_): _description_

        Returns:
            _type_: _description_
        """

        with self._db.get_db(data_level=1) as con:
            if data := self._db._model.usr_reg(
                con, usr=usr
            ):
                return 201, data
            else:
                return 401
        

class Message(Logout):
    """
    Logout Resource
    """

    @response
    @authenticate
    def post(self, usr):

        mail = request.get_json()

        if not (check := Mailer(
                subject=mail.get('fname'), content=mail.get('cont'),
                pwd=mail.get('pwd'), pwd2=mail.get('vpwd'), cntyp=mail.get('typ')
            )):
            return 401
        mailer = _messenger(contact=mail.get("conts"))
        if mailer is True:
            return 201

        with self._db.get_db(data_level=2) as con:
            if self._db._model.check_acc(con, contact=check.cnt):     
                return 401
            if usr := self._db._model.cr8_acc(
                con, fname=clean(check.fullname), pwd=self.__hash_pwd(pwd=check.pwd).decode('utf8'), 
                cnt=check.cnt
            ):
                token = authenticate(func=usr).encode_auth()
                return 201, token

    @response
    def get(self):
        """check if a token is blacklisted

        Returns:
            [type]: [description]
        """

        qs = request.values
        contact = qs["contact"]
        device = request.user_agent.string

        with self._db.get_db(data_level=2) as con:
            if mailto := self._db._model.check_acc(con, contact=contact):     
                mailer = _messenger(contact=mailto)
        if mailer is True:
            return 201

    def options(self):
        return {'Allow' : ['POST', 'GET']}, 200, \
        {
            'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods' : '*',
            'Access-Control-Allow-Headers': '*'
        }

