

from flask_restful import Api
from flask import Blueprint

from setApp import csrf
from .geo import IpRegistry, Geodata


geo = Blueprint('geo', __name__, "/geodata")
geoAPI = Api(app=geo, decorators=[csrf.exempt])


geoAPI.add_resource(IpRegistry, '/signature')
geoAPI.add_resource(Geodata, '/places')
