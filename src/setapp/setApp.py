from flask import Flask, g, render_template, request, url_for

# from flask_fontawesome import FontAwesome
from setting.helper import FormData


def setAp(config: str) -> Flask:
    accounts: Flask = Flask(__name__)
    accounts.jinja_env.filters["formData"] = FormData

    accounts.config.from_pyfile(config)
    # FontAwesome(accounts)

    # spot.config.from_object(config)
    return accounts


setApp = setAp(config="../config.py")


@setApp.route("/")
def index() -> render_template:
    # return "this page is loading"
    data: list[dict[str, dict[str, object]]] = [
        {
            "usr": {
                "id": 2,
                "fname": "John",
                "lname": "Mba",
                "pix": "static/media/mypix.JPEG",
            },
            "spot": {
                "id": 1,
                "arena": "name of the arena",
                "affair": "Electoral fraud",
                "titl": "the tittle of the article, click to read in full",
                "media": "/static/media/vidtest.mp4",
                "detail": """
                Achieving this through cross pollination and/or
                breeding is limited by the fact that pollination and
                cross breeding occurs only between same or closely related
                species. Achieving this through cross pollination and/or
                breeding is limited by the fact that pollination and cross
                breeding occurs only between same or closely related species.
            """,
            },
        }
    ]
    return render_template(
        "/pages/home.html",
        limelits=data,
        endpt=url_for("accs.regs.signInPage"),
        fields="login",
    )


@setApp.before_request
def geodata() -> None:
    print(request.remote_addr)
    # ip_api = f"
    # https://api.ipgeolocation.io/ipgeo?apiKey=24ec8cbc4aa045109d74a354480e3edb&ip=41.58.245.88"

    # georeq = requests.post(
    # url=" http://127.0.0.1:3000/geoip/signature",
    # data={"remadr": "41.58.245.88"}
    # )
    # print(georeq.json())


@setApp.teardown_appcontext
def teardown_db() -> None:
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


accounts = setApp
