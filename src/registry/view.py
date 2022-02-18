
import json

from flask import render_template, url_for, redirect, Blueprint, request, session

from setting.helper import ReqApi, form_dict


regs = Blueprint('regs', __name__, url_prefix="/registry")

@regs.get("/finalize")
def finalPage():
    
    data = ReqApi(req_typ="get", req_url="/accounts/api/reg")
    data = data()

    if data.is_redirect:
        return data
    if not data.ok:
        return data
    data = data.json()
    print(data)
    return render_template('registry/finalReg.html', data=data.get("row_to_json"))

@regs.post("/finalize")
def finalize():

    post_data = json.dumps(request.form)
    data = ReqApi(req_typ="put", req_url="/accounts/api/reg", post_data=post_data)
    data = data()

    if data.is_redirect:
        return data
    if not data.ok:
        return data
    return redirect(url_for('grocs.groc.pixs'))

@regs.post("/register")
def register():

    post_data = json.dumps(request.form)
    data = ReqApi(req_typ="post", req_url="/accounts/api/reg", post_data=post_data)
    data = data()

    if not data.ok:
        return data
    data = data.json()

    if data:
        session["token"] = data
        return redirect(url_for('accs.regs.finalize'))
    return redirect(request.url)

@regs.get("/register")
def regPage():
    return render_template('/registry/reg.html', hide_btn="d-block", btn_href="/")

@regs.get("/reset")
def resetPage():
    
    form_attr, inputs = form_dict(endpt="accs.regs.reset", fields=["Contact"])

    return render_template('registry/recovery.html', inputs=inputs, form_attr=form_attr, hide_btn="d-block", btn_href="/")

@regs.post("/reset")
def reset():

    post_data = json.dumps(request.form)
    data = ReqApi(req_typ="put", req_url="rega.login", post_data=post_data)

    data = data()

    if not data.ok:
        return data
    elif data.ok:
        redirect(url_for('accounts.accs.regs'))
    redirect(url_for('profiler.basics'))

@regs.get("/signIn")
def signInPage():
    return render_template('registry/log.html', hide_btn="d-block", btn_href="/Accounts/logIn")

@regs.post("/signIn")
def signIn():

    post_data = request.form
    auth = (post_data['usrCont'], post_data['usrPwd'])
    data = ReqApi(req_typ="post", req_url=url_for('rega.login'), post_data=auth)
    data = data()

    if not data.ok:
        return data
    data = data.json()
    
    if data.get("token_status") is True:
        "api insert request to other tieters"
        return redirect(url_for('localhost:3000'))
    session["token"] = data["token"]
    if data.get("user_status") is False:
        return redirect(url_for('accs.regs.finalize'))
    elif data.get("user_status") is True:
        return redirect(url_for('localhost:3000'))
    return redirect(url_for('accs.regs.regPage'))

@regs.get("/logOut")
def confLogOut():
    
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

@regs.post("/logOut")
def logOut():
    if request.method == "POST":
        #logout(request)
        return redirect("/login")
    context = {
        "form": None,
        "description": "Are you sure you want to logout?",
        "btn_label": "Click to Confirm",
        "title": "Logout"
    }
    return render_template("accounts/auth.html", context)