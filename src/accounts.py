from profile.urls import profs

from registry.urls import accs
from setapp.setApp import accounts
from user.urls import usrs

accounts.register_blueprint(accs, url_prefix="/accounts")
accounts.register_blueprint(profs, url_prefix="/profiles")
accounts.register_blueprint(usrs, url_prefix="/users")


if __name__ == "__main__":
    # import secrets
    # import string
    #
    # alphabet = string.ascii_letters + string.digits
    # while True:
    #    password = "".join(secrets.choice(alphabet) for i in range(20))
    #    if (
    #        any(c.islower() for c in password)
    #        and any(c.isupper() for c in password)
    #        and sum(c.isdigit() for c in password) >= 3
    #    ):
    #        break
    accounts.run(host="0.0.0.0", debug=True)
