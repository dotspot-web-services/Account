
from flask import flash, render_template, url_for, redirect, Blueprint, request, session

from .api.registry import Register, Login, Reset


regs = Blueprint('regs', __name__, url_prefix="/registry")

__REG = Register()
__LOG = Login()
__RESET = Reset()
 

@regs.route("/finalize", methods=["POST", "GET"])
def finalize():

    if (status, data := __REG.get()) and status == 401:
        flash(message="You are not logged in")
        return redirect("/")
    elif data.get("status") is True and data.get("dob") is not None:
        exp = session.get(exp, None)
        flash(
            message=f"This account is not yet activated, please verify your contact or or it will be deleted in{exp}",
            category="warning"
        )
        return render_template('registry/finalReg.html', data=data)
    
    error, status = __REG.put()
    
    if status == 200:
        session["create_profile"] = True
        return redirect(url_for('grocs.groc.pix'))
    if status == 401:
        flash("You are not Logged in or account is deleted ")
        return redirect("/")
    if status == 422:
        data = request.form
        return render_template('registry/finalReg.html', data=data, error=error)

@regs.route(rule="/register", methods=["GET", "POST"])
def regPage():
    
    if request.method == "GET":
        return render_template('/registry/reg.html', endpt=url_for('accs.regs.regPage'), fields="register")

    error, status = __REG.post()
    if status == 201:
        session["active"] = False
        session["token"] = data
        return redirect(url_for('accs.regs.finalize'))
    if status == 422:
        data = request.form
        return render_template('/registry/reg.html', endpt=url_for('accs.regs.regPage'), fields="register", data=data, error=error)
    if status == 409:
        flash(message="Account already exists, please login", category="info")
        data = request.form
        error['form'] = error['message']
        return render_template('/registry/reg.html', endpt=url_for('accs.regs.regPage'), fields="register", data=data, error=error)
        #return  redirect(request.url)

@regs.route(rule="/contact", methods=["GET", "POST"])
def contactPage():
    
    if request.method == "GET":
        return render_template('registry/recovery.html', endpt=url_for("accs.regs.contactPage"), fields="Contact")

    error, status = __RESET.post()

    if status == 200:
        flash(
            message="A reset link has been sent to your Email",
            category="info"
        )
        return redirect(url_for('index'))
    if status == 404:
        data = request.form   
        return render_template(
            'registry/recovery.html', endpt=url_for("accs.regs.contactPage"), fields="Contact", data=data, error=error
        )

@regs.route(rule="/reset", methods=["GET", "POST"])
def resetPage():
    
    if request.method == "GET":
        return render_template(
            'registry/recovery.html', endpt=url_for("accs.regs.resetPage"), fields="recover"
        )

    error, status = __LOG.put()

    if status == 200:
        flash(message="Password changed successfully", category="message")
        return redirect("/")
    elif status == 422:
        data = request.form
        return render_template(
            'registry/recovery.html', endpt=url_for("accs.regs.resetPage"), fields="recover", data=data, error=error
        )

@regs.route(rule="/signIn",  methods=["GET", "POST"])
def signInPage():
    
    if request.method == "GET":
        return render_template(
            'registry/log.html', endpt=url_for('accs.regs.signInPage'), fields="login"
        )
    
    err_data, status = __LOG.post()

    if status == 200:
        session["token"] = err_data["token"]
        session["create_profile"] = True
        flash(message=f"Logged in successfully", category="message")
        return redirect(url_for('grocs.groc.pix'))
    elif status == 401:
        data = request.form
        flash(message=f"Log in not successfully", category="warning")
        return render_template(
            'registry/log.html', endpt=url_for('accs.regs.signInPage'), fields="login", data=data, error=err_data
        )

@regs.route(rule="/logOut", methods=["GET", "POST"])
def confLogOut():
    
    if request.method == "POST":
        session.clear()
        return redirect("/")
    context = {
        "form": None,
        "description": "Are you sure you want to logout?",
        "btn_label": "Click to Confirm",
        "title": "Logout"
    }
    return render_template(request, "accounts/auth.html", context)
