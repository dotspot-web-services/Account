
from flask_restful import Api
from flask import Blueprint

from profile.prof import Basic, Advanced,  Resacher, Workplace


profBp = Blueprint('event', __name__)
profAp = Api(app=profBp)

profAp.add_resource(resource=Basic, urls='/Basics')
profAp.add_resource(resource=Advanced, urls='/Advanced')
profAp.add_resource(resource=Resacher, urls='/Researcher')
profAp.add_resource(resource=Workplace, urls='/Works')