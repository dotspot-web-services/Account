
from flask import Flask, render_template, g
from flask_wtf.csrf import CSRFProtect



def setAp(config):
    accounts = Flask(__name__)
    accounts.config['SECRET_KEY'] = 'secret'
    csrf = CSRFProtect(accounts)
    accounts.config.from_pyfile(config)
    #spot.config.from_object(config)
    return accounts, csrf

setApp, csrf = setAp(config='config.py')

@setApp.route("/")
def index():
    #return "this page is loading"
    return render_template("/pages/home.html")

@setApp.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

accounts = setApp