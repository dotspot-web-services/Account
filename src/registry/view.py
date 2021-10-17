
from flask import render_template, redirect, wrappers

from setting.decs import Auths as authenticate
from setting.dbcon import DbSet


@authenticate
def finish(usr):
    db = DbSet()

    if isinstance(usr, wrappers.Response):
        return usr
    with db.get_db() as con:
        data = db._model.complete_reg(
            con, usr=usr
        )

    form_attr = {
        "method": "POST", "action": "/src", "class": "form-inline my-2 my-lg-0",
    "button": { "class": "btn btn-outline-success my-2 my-sm-0", "label": "Submit"}
    }
    inputs = {
        'Full name': {"type": "text", "name": "dspln", "class": "form-control"}, 'Contact': {"type": "text", "name": "plc", "class": "form-control"}, 
        'Birthday': {'type': 'date', "class": "form-control"}, 'Gender': {"labels":{'Male': {'value': 1}, 'female': {'value': 0}}, "type": "radio"}
    }
    return render_template('profiles/profile.html', inputs=inputs, form_attr=form_attr, data=data)

def reset():
    form_attr = {
        "method": "POST", "action": "/src", "class": "form-inline my-2 my-lg-0",
    "button": { "class": "btn btn-outline-success my-2 my-sm-0", "label": "Submit"}
    }
    inputs = {'Contact': {"type": "text", "name": "plc", "class": "form-control"}}
    return render_template('registry/recovery.html', inputs=inputs, form_attr=form_attr, hide_btn="d-block", btn_href="/")

def regPage():
    return render_template('registry/reg.html', hide_btn="d-block", btn_href="/")

def signIn():
    return render_template('registry/log.html', hide_btn="d-block", btn_href="/Accounts/logIn")

def logOut(request, *args, **kwargs):
    if request.method == "POST":
        #logout(request)
        return redirect("/login")
    context = {
        "form": None,
        "description": "Are you sure you want to logout?",
        "btn_label": "Click to Confirm",
        "title": "Logout"
    }
    return render_template(request, "accounts/auth.html", context)