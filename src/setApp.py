import requests

from flask import Flask, render_template, g, request, url_for
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

@setApp.before_first_request
def geodata():
    print(request.remote_addr)
    #ip_api = f"https://api.ipgeolocation.io/ipgeo?apiKey=24ec8cbc4aa045109d74a354480e3edb&ip=41.58.245.88"

    #georeq = requests.post(url=" http://127.0.0.1:3000/geoip/signature", data={"remadr": "41.58.245.88"})
    #print(georeq.json())


@setApp.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

accounts = setApp