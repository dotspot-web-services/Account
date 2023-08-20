
from flask import Blueprint

from .views import prof
from .api.url import profBp

profs = Blueprint('profs', __name__, "profile")



profs.register_blueprint(profBp, url_prefix="/api")
profs.register_blueprint(prof, url_prefix="/app")

