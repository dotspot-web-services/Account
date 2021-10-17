
from flask_restful import Api
from flask import Blueprint
from .registry import Login, Logout, Register


registryBp = Blueprint('registry', __name__)

#@registryBp.after_request
#def after_request(response):
#    response.headers.add('Access-Control-Allow-Origin', '*')
#    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
#    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
#    return response

registryApi = Api(app=registryBp)
registryApi.add_resource(Register, '/reg')
registryApi.add_resource(Login, '/login')
registryApi.add_resource(Logout, '/logout')
