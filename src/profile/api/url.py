
from flask_restful import Api
from flask import Blueprint

from setApp import csrf
from .prof import Basic, Accademics,  Resacher, Works



profBp = Blueprint('profa', __name__, url_prefix="/profiler")
profAPI = Api(app=profBp, decorators=[csrf.exempt])


profAPI.add_resource(Basic, '/Basics')
profAPI.add_resource(Accademics, '/Accademics')
profAPI.add_resource(Resacher, '/Researcher')
profAPI.add_resource(Works, '/Works')