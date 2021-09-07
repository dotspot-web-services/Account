
import bcrypt
from bleach import clean

from flask_restful import Resource
from flask import make_response, request, jsonify


from registry.registrySerializer import  (
    RegCheck, LogCheck
)
from setting.decs import Auth, Cors as corsify
from setting.dbcon import DbSet

class Register(Resource):
    """
    User Registration Resource
    """
    def __init__(self):
        self._db = DbSet()

    def __hash_pwd(self,pwd):
        return bcrypt.hashpw(bytes(pwd, encoding='utf-8'), bcrypt.gensalt(self._db._oda.log_rod)
        )

    @corsify
    def post(self):
        # get the post data
        reg_data = request.get_json()
        
        check = RegCheck(
            fullname=reg_data.get('fname'), cnt=reg_data.get('cont'), dob=reg_data.get('dob'),
            pwd=reg_data.get('pwd'), pwd2=reg_data.get('pwd2'), cntyp=reg_data.get('typ'),
            sex=reg_data.get('sx')
        )
        user = self._db._model.in_acc(
            self._db.get_db(), fname=clean(check.fullname), bday=check.dob, mel=check.sex, 
            pwd=self.__hash_pwd(pwd=check.pwd).decode('utf8'), cnt=check.cnt, emel=check.cntyp
            )

        if not user:
            return make_response(jsonify({'status': 'failed', 'message': 'user already exist'}), 401)
        try:
            # generate the auth token
            responseObject = {
                'status': 'success',
                'message': 'Successfully registered.',
                'auth_token': Auth(func=user).encode_auth()
            }
            return make_response(
                jsonify(responseObject), 201
            )
        except Exception as e:
            responseObject = {
                'status': 'fail',
                'message': f'Some error occurred {e}. Please try again.'
            }
            return make_response(
                jsonify(responseObject), 401
            )

    @corsify
    def get(self):
        "this is a get request, it's reachable", 201
        

class Login(Register):
    """
    User Login Resource
    """

    @corsify
    def post(self):
        # get the post data

        auth = request.authorization
        if not auth or not auth.username or not auth.password:
            return make_response(
                jsonify({'WWW.Authenticate': 'Basic realm="login required"'}), 401
            )
        check = LogCheck(
                cnt=auth.username, pwd=auth.password
            )
        usr = self._db._model.check_acc(self._db.get_db(dict=True), contact=check.cnt) # fetch user external id
        try:

            if not usr:              
                return jsonify({'WWW.Authenticate': 'Basic realm="login required"'}), 401
            if not bcrypt.checkpw(password=check.pwd.encode('utf-8'), hashed_password=usr[0].get('pwd').encode('utf-8')):
                return jsonify({'WWW.Authenticate': 'Basic realm="login required"'}), 401

            token = Auth(func=usr[0].get('usr')).encode_auth()
            if token:
                return jsonify({'token': f'{token}'})
        except Exception as e:
            return jsonify({'message' : f'could not verify, Basic realm="encounted: {e}'}), 401

    @corsify
    def get(self):
        return "this is a get request, it login is reachable", 201


class Logout(Resource):
    """
    Logout Resource
    """
    db = DbSet()

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
            