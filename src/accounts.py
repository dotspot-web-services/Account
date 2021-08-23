
from flask import Flask

from registry.urls.url import registryBp
from profile.urls.url import profBp
from user.urls.url import groceBp


def setAp(config):
    accounts = Flask(__name__)

    #spot.config.from_object(config)
    accounts.config.from_pyfile(config)
    accounts.register_blueprint(registryBp, url_prefix="/Registry")
    accounts.register_blueprint(profBp, url_prefix="/Profiles")
    accounts.register_blueprint(groceBp, url_prefix="/Groceries")

    return accounts

if __name__ == "__main__":
    accounts = setAp('config.py')
    accounts.run(debug=True)