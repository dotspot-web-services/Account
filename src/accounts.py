
from flask import Flask, render_template, g

#from registry.api.url import registryBp
from registry.api.url import registryBp
from profile.api.url import profBp
from profile.urls import profs
from user.urls.url import groceBp
from registry.urls import accs


def setAp(config):
    accounts = Flask(__name__)

    @accounts.route("/")
    def index():
        form_attr = {
            "method": "POST", "action": "/src", "class": "form-inline my-2 my-lg-0",
        "button": { "class": "btn btn-outline-success my-2 my-sm-0", "label": "Search"}
        }

        inputs = {
                'search': {'placeholder': 'Find your quest in arena', "type": "text", "name": "srch", "id": "srch", "class": "form-control mr-sm-2"}, 
            }
        return render_template(
            'pages/home.html', inputs=inputs, form_attr=form_attr, form_cls="form-inline", hide_btn="d-none"
        )
        
    #spot.config.from_object(config)
    accounts.config.from_pyfile(config)
    accounts.register_blueprint(registryBp, url_prefix="/Registry")
    accounts.register_blueprint(accs, url_prefix="/Accounts")
    accounts.register_blueprint(profBp, url_prefix="/Profilers")
    accounts.register_blueprint(profs, url_prefix="/Profiles")
    accounts.register_blueprint(groceBp, url_prefix="/Groceries")
    return accounts

if __name__ == "__main__":
    accounts = setAp('config.py')
    accounts.run(debug=True)  

    @accounts.teardown_appcontext
    def teardown_db(exception):
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()