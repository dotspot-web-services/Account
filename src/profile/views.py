
from flask import render_template, url_for, redirect, Blueprint, request, session, flash

from .api.prof import Basic, Accademics,  Resacher, Works


prof = Blueprint('prof', __name__, url_prefix="/profile")


__BS = Basic() 
__ACAD = Accademics() 
__RSCH = Resacher()
__WRK = Works()


@prof.route("/basics", methods=["GET", "POST"])
def basics():
    "user bsic knowledge profile"
    
    skip = url_for("profs.prof.work")
    desc = {
        "radio": "choose skilled if it's gotten in school and unskilled if not", 
        "dspln": "<div><span>skilled</span> could be any non universial tertiary education grouping of knowledge</div> <div><span>unskilled</span> could be from an accademy grouping of knowledge</div>",
        "class": "note"
    }
    data, status = __BS.get()
    if status == 401:
        flash(message="You are not logged in")
        return redirect("/")
    elif request.method == "GET":
        return render_template(
            'profiles/profile.html', endpt=url_for('profs.prof.basics'), fields="basic", desc=desc, data=data, skip=skip 
        )

    data, status = __BS.post()
    
    if status == 200 and session["create_profile"]:
        return redirect(url_for('profs.prof.acads'))
    if status == 200:
        return redirect(url_for("grocs.groc.prof"))
    if status == 422:
       return render_template(
            'profiles/profile.html', endpt=url_for('profs.prof.basics'), fields="basic",
            desc=desc, skip=skip, data=data
        )
    if status == 409:
        flash(message="Account already exists, please login", category="info")
        return  redirect(request.url)

@prof.route("/academics",  methods=["GET", "POST"])
def acads():
    """user universal accedemic profile"""
    
    skip = url_for("profs.prof.work")
    desc = "Accademic profile is subject to verification"
    
    if (data, status := __BS.get()) and status == 401:
        flash(message="You are not logged in")
        return redirect("/")
    elif status == 401 and data.get("acad") == False:
        return redirect(skip)
    if request.method == "GET" and (data, status := __ACAD.get()):
        return render_template(
            'profiles/profile.html', endpt=url_for("profs.prof.acads"), fields="Accademic", desc=desc, skip=skip 
        )
    
    data, status = __ACAD.post()
    
    if status == 200 and session["create_profile"]:
        return redirect(url_for('profs.prof.resrch'))
    if status == 200:
        return redirect(url_for("grocs.groc.prof"))
    elif status == 422:
       return render_template(
            'profiles/profile.html', ndpt=url_for('profs.prof.acads'), fields="Accademic", desc=desc, skip=skip, data=data
        )
    elif status == 409:
        flash(message="Account already exists, please login", category="info")
        return  redirect(request.url)

@prof.route("/researchs",  methods=["GET", "POST"])
def resrch():
    
    note = {"org": "this could be an accademic research work", "emel": "This must be an organisation or institution email. It's subject to verification"}
    skip = "/profiles/app/works"
    desc = "fill up the profile below as a researcher with respect to organisation or institution of research"
    
    if (data, status := __RSCH.get()) and status == 401:
        flash(message="You are not logged in")
        return redirect("/")
    elif request.method == "GET":
        return render_template(
            'profiles/profile.html', endpt=url_for("profs.prof.resrch"), fields="research", desc=desc, skip=skip 
        )
        
    data, status = __BS.post()
    
    if status == 200 and session["create_profile"]:
        return redirect(url_for('profs.prof.work'))
    if status == 200:
        return redirect(url_for("grocs.groc.prof"))
    elif status == 422:
       return render_template(
            'profiles/profile.html', ndpt=url_for('profs.prof.resrch'), fields="research", desc=desc, skip=skip, data=data
        )
    elif status == 409:
        flash(message="Account already exists, please login", category="info")
        return  redirect(request.url)

@prof.route("/works",  methods=["GET", "POST"])
def work():

    skip = '/profiles/app/profile'
    desc = "fill work experience in other to share and mentor, you take what you give"
    data, status = __WRK.get()
    
    if status == 401:
        flash(message="You are not logged in")
        return redirect("/")
    elif request.method == "GET":
        return render_template(
            'profiles/profile.html', endpt=url_for("profs.prof.work"), fields="work", desc=desc, skip=skip
        )
        
    data, status = __BS.post()
    if status == 200:
        return redirect(url_for("grocs.groc.prof"))
    elif status == 422:
       return render_template(
            'profiles/profile.html', ndpt=url_for('profs.prof.work'), fields="work", desc=desc, skip=skip, data=data
        )
    elif status == 409:
        flash(message="Account already exists, please login", category="info")
        return  redirect(request.url)
