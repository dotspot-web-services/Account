
import bcrypt

from flask import jsonify, make_response, request, render_template, redirect, url_for
from flask_restful import Resource
from bleach import clean
from werkzeug import Response

from ..serializer import RegCheck, LogCheck, finalCheck, PwdCheck, Ip, Globe
from setting.decs import Auth as authenticate
from setting.helper import ApiResp
from setting.dbcon import DbSet

class Register(Resource):
    """
    User Registration Resource
    """
    
    def __init__(self):
        self._db = DbSet()

    def __hash_pwd(self,pwd):
        return bcrypt.hashpw(
            bytes(pwd, encoding='utf-8'), bcrypt.gensalt(self._db._oda.log_rod)
        )

    def post(self):

        reg_data = request.get_json()
        print(reg_data)
        if not (check := RegCheck(
                fullname=reg_data.get('fname'), cnt=reg_data.get('cont'),
                pwd=reg_data.get('pwd'), pwd2=reg_data.get('vpwd'), cntyp=reg_data.get('typ')
            )):
            return ApiResp(status_code=401)

        with self._db.get_db(data_level=2) as con:
            if self._db._model.check_acc(con, self._db.get_db(), contact=check.cnt):     
                return ApiResp(status_code=401)
            if usr := self._db._model.cr8_acc(
                con, fname=clean(check.fullname), pwd=self.__hash_pwd(pwd=check.pwd).decode('utf8'), 
                cnt=check.cnt
            ):
                token = authenticate(func=usr).encode_auth()
                return ApiResp(status_code=201, data=token)

    @authenticate
    def put(self, usr, token_status):

        if isinstance(usr, tuple):
            usr = usr.usr
        elif isinstance(token_status, Response):
            return usr

        reg_data = request.get_json()

        if not (check := finalCheck(
                fullname=reg_data.get('fname'), cnt=reg_data.get('cont'), dob=reg_data.get('dob'),
                cntyp=reg_data.get('typ'), sex=reg_data.get('sx')
            )):
            return ApiResp(status_code=401)
        with self._db.get_db() as con:
            if not self._db._model.upd8_acc(
                con, usr=usr, fname=clean(check.fullname),cnt=check.cnt, emel=check.cntyp,
                bday=check.dob, mel=check.sex, actv=True, verfd= True
            ):
                return ApiResp(status_code=201)
            else:
                return ApiResp(status_code=401)

    @authenticate
    def get(self, usr, token_status):
        """check if a user already exists"""

        if isinstance(usr, tuple):
            usr = usr.usr
        elif isinstance(token_status, Response):
            return usr

        with self._db.get_db(data_level=1) as con:
            if data := self._db._model.usr_reg(
                con, usr=usr
            ):
                return ApiResp(status_code=201, data=data)
            else:
                return ApiResp(status_code=401)

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

    def post(self):
        # get the post data

        auth = request.authorization
        contact = auth.username
        password = auth.password
    
        if not contact or not password:
            return ApiResp(status_code=401)
            
        if not (check := LogCheck(
                cnt=contact, pwd=password
            )):
            return ApiResp(status_code=401)

        with self._db.get_db(data_level=2) as con:
            if not (usr := self._db._model.check_acc(con, contact=check.cnt)):
                return ApiResp(status_code=401)
        
        if bcrypt.checkpw(password=check.pwd.encode('utf-8'), hashed_password=usr.pwd.encode('utf-8')):
            with self._db.get_db(data_level=1) as con:   
                if not (usr_data := self._db._model.usr_status(con, contact=check.cnt)):
                    token = authenticate(func=usr.usr).encode_auth(status=False)
                    usr_data["token"] = token
                if usr_data["token_status"] is True:
                    return ApiResp(status_code=401)
                if usr_data["token"] is not None:
                    self._db._model.del_tkn(con, tkn=usr_data["token"])
            return make_response(jsonify(usr_data), 201)
        return ApiResp(status_code=401)

    def get(self):
        """check if a user already exists"""

        qs = request.values
        contact = qs["contact"]

        with self._db.get_db() as con:
            if cont := self._db._model.get_cont(
                con, cnt=contact
            ):
                return ApiResp(status_code=201, data=cont)
            else:
                return ApiResp(status_code=401)

    @authenticate
    def put(self, usr, token_status=None):
        
        if token_status:
            redirect(url_for('accs.regs.finalize'))
        reg_data = request.get_json()
        
        if not (check := PwdCheck(cnt=reg_data.get('cont'),
                pwd=reg_data.get('pwd'), pwd2=reg_data.get('vpwd')
            )):
            return ApiResp(status_code=401)

        with self._db.get_db() as con:
            if not self._db._model.upd8_pwd(
                con, usr=usr, pwd=self.__hash_pwd(pwd=check.pwd).decode('utf8')
            ):
                return ApiResp(status_code=201)
            else:
                return ApiResp(status_code=401)

class Logout(Resource):
    """
    Logout Resource
    """
    def __init__(self):
        self._db = DbSet()

    @authenticate
    def post(self, usr):
        # get auth token
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            check_token = authenticate(func=auth_token).decode_auth()
            if not isinstance(check_token, str):
                with self._db.get_db() as con:
                    self.db._model.in_tkn(con, tkn=auth_token, usr=usr)
                    return ApiResp(status_code=201)
            else:
                return ApiResp(status_code=401)
        else:
            return ApiResp(status_code=403)

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

class Geodata(Logout):
    """
    basic education or acquired skill
    """

    @authenticate
    def post(self, usr):
        # get the post data
        prof_data = request.get_json() or request.form
        print(prof_data)
        if not (check:= Globe(
                    dspln=prof_data.get('dspln'), place=prof_data.get('plc'),
                    strtd=prof_data.get('strt'), endd=prof_data.get('end')
                )):
            return ApiResp(status_code=401)
        try:
            with self._db.get_db() as con:
                self._db._model.in_work(
                    con, usr=usr, dspln=clean(check.dspln), plc=clean(check.place),
                    strtd=check.strtd, endd=check.endd,
                )
            return ApiResp(status_code=201)
        except Exception:
            return ApiResp(status_code=401)

    @authenticate
    def get(self, usr):
        """reset password"""
        acad = Ip(self._db._model.basic_prof(
            self._db.get_db(dict=True), contact=usr
        ))

        if acad:
            form = {
                'organisation': {'value': ''}, 'role': {'value': ''},
                'started': {'type': 'date'}, 'Ended': {'value': 1}
            }
        return render_template('pages/home.html', form=form)
