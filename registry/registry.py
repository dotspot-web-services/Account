
from flask_restful import Resource
from flask import make_response, request, jsonify
import bleach
import bcrypt

from registry.registrySerializer import  (
    RegCheck, LogCheck
)
from setting.dbcon import DbSet as db, Auth


class Register(Resource):
    """
    User Registration Resource
    """

    @staticmethod
    def __hash_pwd(pwd):
        return bcrypt.hashpw(pwd, bcrypt.gensalt(db.oda.log_rod)
        ).decode()

    def post(self):
        # get the post data
        reg_data = request.get_json()
        
        check = RegCheck(
            fullname=reg_data.get('fname'), cnt=reg_data.get('cont'), dob=reg_data.get('dob'),
            pwd=reg_data.get('pwd'), pwd2=reg_data.get('pwd2'), cntyp=reg_data.get('typ')
        )

        if not db._model.check_acc(db, contact=check.cnt): 
            return make_response({'status': 'failed', 'message': 'user already exist'}, 401)

        try:
            user = db._model.in_acc(
                db, ip=check.ip, fname=bleach(check.fullname), dob=check.dob, gend=check.sex, 
                dtd=check.dt, cnt=check.cnt, pwd=self.__hash_pwd(ped=check.pwd), cntyp=check.cntyp
            )
            # generate the auth token
            auth_token = Auth.encode_auth(user.usrid)
            responseObject = {
                'status': 'success',
                'message': 'Successfully registered.',
                'auth_token': auth_token.decode()
            }
            return make_response(jsonify(responseObject)), 201
        except Exception as e:
            responseObject = {
                'status': 'fail',
                'message': f'Some error occurred {e}. Please try again.'
            }
            return make_response(jsonify(responseObject)), 401

class Login(Resource):
    """
    User Login Resource
    """

    def post(self):
        # get the post data
        auth = request.authorization
        if not auth or not auth.username or not auth.password:
            return make_response('could not verify', 401, {'WWW.Authenticate': 'Basic realm="login required"'})
        check = LogCheck(
                cnt=auth.username, cntyp=auth.password
            )
        usr = db._model.check_acc(db, us=check.cnt) # fetch user external id
        try:

            if not usr:
                return make_response('could not verify', 401, {'WWW.Authenticate': 'Basic realm="login required"'})
            
            if not bcrypt.checkpw(usr.pwd, bcrypt.hashpw(check.pwd, bcrypt.gensalt(db.oda.log_rod))):
                return make_response('could not verify', 401, {'WWW.Authenticate': 'Basic realm="login required"'})
           
            token = Auth.encode_auth(usr = usr.id)
            if token:
                return jsonify({'token': token.decode('UTF-8')})

        except Exception as e:
            print(e)
            make_response('could not verify', 401, {'WWW.Authenticate': f'Basic realm="encounted{e}"'})

    def get():
        """reset password"""


class Logout(Resource):
    """
    Logout Resource
    """

    def post(self):
        # get auth token
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = Auth.decode_auth(auth_token)
            if not isinstance(resp, str):
                try:
                    db._model.in_tkn(db, tkn=auth_token)
                    responseObject = {
                        'status': 'success',
                        'message': 'Successfully logged out.'
                    }
                    return make_response(jsonify(responseObject)), 200
                except Exception as e:
                    responseObject = {
                        'status': 'fail',
                        'message': e
                    }
                    return make_response(jsonify(responseObject)), 200
            else:
                responseObject = {
                    'status': 'fail',
                    'message': resp
                }
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(jsonify(responseObject)), 403
            