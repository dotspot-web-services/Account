
from flask_restful import Api
from flask import Blueprint

from user.grocery import Pubs, Awards, Story, versn


groceBp = Blueprint('grocery', __name__)


groceApi = Api(app=groceBp )
groceApi.add_resource(resource=Pubs, urls='/publications')
groceApi.add_resource(resource=Awards, urls='/awards')
groceApi.add_resource(resource=Story, urls='/stories')
groceApi.add_resource(resource=versn, urls='/versions')