
from flask_restful import Api
from flask import Blueprint

from setApp import csrf
from .grocery import Pubs, Awards, Socs, Avatars, Profiles



groceBp = Blueprint('groca', __name__)


groceAPI = Api(app=groceBp, decorators=[csrf.exempt])

groceAPI.add_resource(Pubs, '/publications')
groceAPI.add_resource(Awards, '/awards')
groceAPI.add_resource(Socs, '/socials')
groceAPI.add_resource(Avatars, '/pictures')
groceAPI.add_resource(Profiles, '/profiles')
