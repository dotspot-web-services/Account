
from flask_restful import Api
from flask import Blueprint
from registry.registry import Login, Logout, Register


registryBp = Blueprint('registry', __name__)

registryApi = Api(app=registryBp)
registryApi.add_resource(Register, '/reg')
registryApi.add_resource(Login, '/login')
registryApi.add_resource(Logout, '/logout')