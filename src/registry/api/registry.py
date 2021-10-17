
import bcrypt
from bleach import clean

from flask_restful import Resource

from setting.decs import Auth as authenticate
from flask.views import MethodView
from flask import (
    make_response, request, jsonify, render_template, 
    redirect, url_for, session, 
)


from ..serializer import  (
    RegCheck, LogCheck
)
from setting.decs import Auth, Cors as corsify
from setting.dbcon import DbSet

class Register(MethodView):
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

        reg_data = request.form
        #reg_data = reg_data.get('content')
        
        check = RegCheck(
            fullname=reg_data.get('fname'), cnt=reg_data.get('cont'),
            pwd=reg_data.get('pwd'), pwd2=reg_data.get('vpwd'), cntyp=reg_data.get('typ')
        )
        with self._db.get_db() as con:
            user = self._db._model.in_acc(
                con, fname=clean(check.fullname), pwd=self.__hash_pwd(pwd=check.pwd).decode('utf8'), 
                cnt=check.cnt, emel=check.cntyp
            )

        if not user:
            return make_response(jsonify({'status': 'failed', 'message': 'user already exist'}), 401)
        try:
            # generate the auth token
            token = Auth(func=user).encode_auth()
            resp = {
                'status': 'success',
                'message': 'Successfully registered.',
                'auth_token': token
            }
            status_code = 201
        except Exception as e:
            resp = {
                'status': 'fail',
                'message': f'Some error occurred {e}. Please try again.'
            }
            status_code = 401
        finally:
            resp = make_response(jsonify(resp), status_code)
            resp.set_cookie("same-site-cookie", "session", samesite="Lax")
            if not request.is_json:
                session['token'] = token
                return resp
            return redirect(url_for('.register'))

    def get(self):
        return "this page is loading..."

    def put(self):
        # get the post data
        reg_data = request.form
        
        check = RegCheck(
            fullname=reg_data.get('fname'), cnt=reg_data.get('cont'), dob=reg_data.get('dob'),
            cntyp=reg_data.get('typ'), sex=reg_data.get('sx')
        )

        if self._db._model.in_acc(
                self._db.get_db(), fname=clean(check.fullname), bday=check.dob, mel=check.sex, 
                cnt=check.cnt, emel=check.cntyp
            ):
            return make_response(jsonify({'status': 'successful', 'message': 'update done succeesfully'}), 201)
        else:
            return make_response(jsonify({'status': 'failed', 'message': 'user already exist'}), 401)

    def options(self):
        return {'Allow' : ['POST', 'GET']}, 200, \
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

        auth = request.authorization or request.form

        contact = auth.get('usrCont') or auth.username
        password = auth.get('usrPwd') or auth.password
    
        if not contact or not password:
            return make_response(
                jsonify({'WWW.Authenticate': 'Basic realm="login required"'}), 401
            )
            
        check = LogCheck(
                cnt=contact, pwd=password
            )
        usr = self._db._model.check_acc(self._db.get_db(dict=True), contact=check.cnt) # fetch user external id
        try:
            if not usr:              
                return jsonify({'WWW.Authenticate': 'Basic realm="login required"'}), 401
            if not bcrypt.checkpw(password=check.pwd.encode('utf-8'), hashed_password=usr[0].get('pwd').encode('utf-8')):
                return jsonify({'WWW.Authenticate': 'Basic realm="login required"'}), 401

            token = Auth(func=usr[0].get('usr')).encode_auth()
            return jsonify({'token': f'{token}'})
        except Exception as e:
            return jsonify({'message' : f'could not verify, Basic realm="encounted: {e}'}), 401
        finally:
            if not request.authorization:
                print('ok')
                redirect("/Profiles/Basics")

class Logout(Resource):
    """
    Logout Resource
    """
    db = DbSet()

    def get(request, *args, **kwargs):
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

    @corsify
    def post(self):
        # get auth token
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = Auth(func=auth_token).decode_auth()
            if not isinstance(resp, str):
                try:
                    self.db._model.in_tkn(self.db, tkn=auth_token)
                    responseObject = {
                        'status': 'success',
                        'message': 'Successfully logged out.'
                    }
                    return make_response(jsonify(responseObject), 200)
                except Exception as e:
                    responseObject = {
                        'status': 'fail',
                        'message': e
                    }
                    return make_response(jsonify(responseObject), 200)
            else:
                responseObject = {
                    'status': 'fail',
                    'message': resp
                }
                return make_response(jsonify(responseObject), 401)
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(jsonify(responseObject), 403)
            