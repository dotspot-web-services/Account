
from flask import Blueprint

from .view import regPage, signIn, logOut, finish, reset

accs = Blueprint('accounts', __name__)

accs.add_url_rule(rule="/regUsr", endpoint="register", view_func=regPage)
accs.add_url_rule(rule="/", endpoint="completeReg", view_func=finish)
accs.add_url_rule(rule="/logIn", endpoint="signUp", view_func=signIn)
accs.add_url_rule(rule="/logOut", endpoint="signOut", view_func=logOut)
accs.add_url_rule(rule="/reset", endpoint="resetAcct", view_func=reset)
