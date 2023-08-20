
from flask import flash, render_template, redirect, url_for, Blueprint, request, session

from .api.grocery import Awards, Socs, Avatars, Profiles


grocs = Blueprint('groc', __name__, url_prefix="/user")
__AWD = Awards() 
__SOC = Socs() 
__PROPIX = Avatars() 
__PROF = Profiles()


@grocs.route("welcome", methods=["GET", "POST"])
def wlcm():
    
    if request.method == "GET":
        return render_template('pages/wlc.html')
    if session["create_profile"]:
        return redirect(url_for('profs.prof.basics'))

@grocs.route("/award", methods=["GET", "POST"])
def awards():
    desc = "fill work experience in other to share and mentor, you take what you give"
    
    if (status, data := __AWD.get()) and status == 401:
        flash(message="You are not logged in")
        return redirect("/")
    if request.method == "GET":
        return render_template(
            'profiles/profile.html', fields="awards", desc=desc, data=data
        )
        
    status, data = __AWD.post()
    
    if status == 200:
        return redirect(url_for("grocs.groc.prof"))
    if status == 422:
       return render_template(
            'profiles/profile.html', endpt=url_for('grocs.groc.awards'), fields="awards", desc=desc, data=data
        )
    if status == 409:
        flash(message="Account already exists, please login", category="info")
        return  redirect(request.url)

@grocs.route("/social", methods=["GET", "POST"])
def social():
    
    desc = "fill work experience in other to share and mentor, you take what you give"
    
    if (status, data := __SOC.post()) and status == 401:
        flash(message="You are not logged in")
        return redirect("/")
    if request.method == "GET":
        return render_template(
            'profiles/profile.html', endpt=url_for("grocs.groc.social"), fields="work", desc=desc, data=data
        )
        
    status, data = __SOC.post()
    if status == 200:
        return redirect(url_for("grocs.groc.prof"))
    if status == 422:
       return render_template(
            'profiles/profile.html', endpt=url_for('grocs.groc.social'), fields="work", desc=desc, data=data
        )
    if status == 409:
        flash(message="Account already exists, please login", category="info")
        return  redirect(request.url)

    
@grocs.route("pix", methods=["GET", "POST"])
def pix():

    status, data = __PROPIX.get()
    desc = "fill work experience in other to share and mentor, you take what you give"
    
    if request.method == "GET":
        return render_template("profiles/pix.html", usr_pix=data, desc=desc)
    
    status, data = __PROPIX.post()
    
    if status == 200 and session["create_profile"]:
        return redirect(url_for('grocs.groc.awards'))
    if status == 200:
        return render_template("profiles/pix.html", desc=desc )
    if status == 422:
       return render_template("profiles/pix.html", desc=desc, data=data)
    if status == 409:
        flash(message="Account already exists, please login", category="info")
        return  redirect(request.url)

@grocs.get("profile")
def prof():
    
    status, data = __PROF.get()
    
    if status == 200:
        return render_template(
            'profiles/profile.html', data=data
        )

