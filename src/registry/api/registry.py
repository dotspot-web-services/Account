
import bcrypt

from flask import jsonify, request, render_template, redirect, url_for
from flask_restful import Resource
from bleach import clean

from ..serializer import RegCheck, LogCheck, finalCheck, PwdCheck, Mailer
from setting.decs import Auth as authenticate, Responders as response
from setting.dbcon import DbSet as _DBSET
from setting.helper import ReqApi
from ..msg import SendMsg as _messenger

class Register(Resource):
    """
    User Registration Resource
    """
    
    def __init__(self):
        self._db = _DBSET()
        self._failed_rits = "Account already exist"
        self._unknown_req = "Unknown API request"

    def __hash_pwd(self,pwd):
        return bcrypt.hashpw(
            bytes(pwd, encoding='utf-8'), bcrypt.gensalt(self._db._oda.log_rod)
        )

    @response
    def post(self):

        reg_data = request.get_json()

        if not (check := RegCheck(
                fullname=reg_data.get('fname'), cnt=reg_data.get('cont'),
                pwd=reg_data.get('pwd'), pwd2=reg_data.get('vpwd'), cntyp=reg_data.get('typ')
            )):
            return 401

        with self._db.get_db(data_level=2) as con:
            if self._db._model.check_acc(con, contact=check.cnt):     
                return 401, self._failed_rits
            if usr := self._db._model.cr8_acc(
                con, fname=clean(check.fullname), pwd=self.__hash_pwd(pwd=check.pwd).decode('utf8'), 
                cnt=check.cnt
            ):
                token = authenticate(func=usr).encode_auth()
                return 201, token

    @response
    @authenticate
    async def put(self, usr, token_status):

        if isinstance(usr, tuple) and usr.usr != 401:
            usr = usr.usr
        else:
            return usr, token_status

        reg_data = request.get_json()

        if not (check := finalCheck(
                fullname=reg_data.get('fname'), cnt=reg_data.get('cont'), dob=reg_data.get('dob'),
                cntyp=reg_data.get('typ'), sex=reg_data.get('sx')
            )):
            return 401
        with self._db.get_db() as con:
            if not self._db._model.upd8_acc(
                con, usr=usr, fname=clean(check.fullname),cnt=check.cnt, emel=check.cntyp,
                bday=check.dob, mel=check.sex, actv=True, verfd= True
            ):
                return 201
            else:
                return 401, self._unknown_req

    @response
    @authenticate
    def get(self, usr, token_status):
        """check if a user already exists"""

        if isinstance(usr, tuple) and usr.usr != 401:
            usr = usr.usr
        else:
            return usr, token_status

        with self._db.get_db(data_level=1) as con:
            if data := self._db._model.usr_reg(
                con, usr=usr
            ):
                return 201, data
            else:
                return 401, self._unknown_req

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
        # get the post data
    
        if not (auth := request.authorization):
            return 401
        contact = auth.username
        password = auth.password
            
        if not (check := LogCheck(
                cnt=contact, pwd=password
            )):
            return 401

        with self._db.get_db(data_level=2) as con:
            if not (usr := self._db._model.check_acc(con, contact=check.cnt)):
                401, self._failed_rits
        
            if bcrypt.checkpw(password=check.pwd.encode('utf-8'), hashed_password=usr.pwd.encode('utf-8')):   
                if not (usr_data := self._db._model.usr_status(con, contact=check.cnt)):
                    token = authenticate(func=usr.usr).encode_auth(status=False)
                    usr_data["token"] = token
                if usr_data["token_status"] is True:
                    401, "Account is not activated yet"
                if usr_data["token"] is not None:
                    self._db._model.del_tkn(con, tkn=usr_data["token"])
                return 201, jsonify(usr_data)
        return 401

    @response
    def get(self):
        """check if a user already exists"""

        qs = request.values
        contact = qs["contact"]

        with self._db.get_db() as con:
            if cont := self._db._model.get_cont(
                con, cnt=contact
            ):
                return 201, cont
            elif not cont:
                return 404, "Not found in resource"
        return 401, self._unknown_req

    @response
    @authenticate
    def put(self, usr, token_status=None):

        if isinstance(usr, tuple) and usr.usr != 401:
            usr = usr.usr
        else:
            return usr, token_status
        
        if token_status:
            redirect(url_for('accs.regs.finalize'))
        reg_data = request.get_json()
        
        if not (check := PwdCheck(cnt=reg_data.get('cont'),
                pwd=reg_data.get('pwd'), pwd2=reg_data.get('vpwd')
            )):
            return 401

        with self._db.get_db() as con:
            if not self._db._model.upd8_pwd(
                con, usr=usr, pwd=self.__hash_pwd(pwd=check.pwd).decode('utf8')
            ):
                return 201
            else:
                return 401, self._unknown_req

class Logout(Resource):
    """
    Logout Resource
    """
    def __init__(self):
        self._db = _DBSET()

    @response
    @authenticate
    def post(self, usr, token_status):
        # get auth token
        if isinstance(usr, tuple) and usr.usr != 401:
            usr = usr.usr
        else:
            return usr, token_status
        
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
    def get(self):
        """check if a token is blacklisted

        Returns:
            [type]: [description]
        """

        if request.method == "POST":
            #logout(request)
            return redirect("/login")
        context = {
            "form": None,
            "description": "Are you sure you want to logout?",
            "btn_label": "Click to Confirm",
            "title": "Logout"
        }
        return render_template(request, "accounts/auth.html", context)

    def options(self):
        return {'Allow' : ['POST', 'GET']}, 200, \
        {
            'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods' : '*',
            'Access-Control-Allow-Headers': '*'
        }

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
                return 401, self._failed_rits
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

