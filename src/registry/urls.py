
from flask import Blueprint

from .view import regs
from .api.url import registryBp

accs = Blueprint('accs', __name__, url_prefix="/account")


accs.register_blueprint(registryBp, url_prefix="/api")
accs.register_blueprint(regs, url_prefix="/app")