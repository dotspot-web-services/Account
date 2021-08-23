
from flask_restful import Api
from flask import Blueprint

from profile.prof import Basic, Accademics,  Resacher, Works


profBp = Blueprint('Accounts', __name__)
profAp = Api(app=profBp)

profAp.add_resource(resource=Basic, urls='/Basics')
profAp.add_resource(resource=Accademics, urls='/Accademics')
profAp.add_resource(resource=Resacher, urls='/Researcher')
profAp.add_resource(resource=Works, urls='/Works')