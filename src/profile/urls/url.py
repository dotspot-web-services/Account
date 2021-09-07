
from flask_restful import Api
from flask import Blueprint

from profile.prof import Basic, Accademics,  Resacher, Works


profBp = Blueprint('Accounts', __name__)
profAp = Api(app=profBp)

profAp.add_resource(Basic, '/Basics')
profAp.add_resource(Accademics, '/Accademics')
profAp.add_resource(Resacher, '/Researcher')
profAp.add_resource(Works, '/Works')