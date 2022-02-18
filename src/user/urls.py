
from flask import Blueprint

from .views import grocs
from .api.url import groceBp


usrs = Blueprint('grocs', __name__)


usrs.register_blueprint(groceBp, url_prefix="/api")
usrs.register_blueprint(grocs, url_prefix="/app")

