
from flask_restful import Api
from flask import Blueprint

from registry.registry import Login, Logout, Register


registryBp = Blueprint('registry', __name__)

registryApi = Api(app=registryBp)
registryApi.add_resource(resource=Register, urls='/reg')
registryApi.add_resource(resource=Login, urls='/login')
registryApi.add_resource(resource=Logout, urls='/logout')