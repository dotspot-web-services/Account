
from flask_restful import Api
from flask import Blueprint

from setApp import csrf
from .registry import Login, Logout, Register


registryBp = Blueprint('rega', __name__, "/registry")
registryAPI = Api(app=registryBp, decorators=[csrf.exempt])


registryAPI.add_resource(Register, '/reg')
registryAPI.add_resource(Login, '/login')
registryAPI.add_resource(Logout, '/logout')
