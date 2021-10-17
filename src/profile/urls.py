
from flask import Blueprint

from .views import basics, acadas, resrcha, works

profs = Blueprint('profiles', __name__)

profs.add_url_rule(rule="/", endpoint="knowledges", view_func=basics)
profs.add_url_rule(rule="/accademics", endpoint="degrees", view_func=acadas)
profs.add_url_rule(rule="/researchers", endpoint="searchers", view_func=resrcha)
profs.add_url_rule(rule="/works", endpoint="working", view_func=works)
