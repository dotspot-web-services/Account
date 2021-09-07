
from flask_restful import Api
from flask import Blueprint

from user.grocery import Pubs, Awards, Story, Versn


groceBp = Blueprint('grocery', __name__)


groceApi = Api(app=groceBp )
groceApi.add_resource(Pubs, '/publications')
groceApi.add_resource(Awards, '/awards')
groceApi.add_resource(Story, '/stories')
groceApi.add_resource(Versn, '/versions')