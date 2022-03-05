
import json

from flask import render_template, url_for, redirect, Blueprint, request

from setting.helper import ReqApi, form_dict


prof = Blueprint('prof', __name__, url_prefix="/profile")


dormain = "http://127.0.0.1:3000/"


@prof.get("/basics")
def basicForm():
    "user bsic knowledge profile"

    data = ReqApi(req_typ="get", req_url=url_for("profa.basic")+"?usr=true")
    base_flds = ['Location', 'Field', 'Knowledge', 'Start', 'End']
    form_attr, inputs = form_dict(endpt=url_for("profs.prof.basics"), fields=base_flds)
    note = {"radio": "choose skilled if it's gotten in school and unskilled if not", 
        "dspln": "<div><span>skilled</span> could be any non universial tertiary education grouping of knowledge</div> <div><span>unskilled</span> could be from an accademy grouping of knowledge</div>",
        "class": "note"
    }
    left_btn_ref = "/accounts/account/app/registry/signIn"
    right_btn_ref = "/profiles/app/academics"
    desc = ""
    data = data()

    if not request.values:
        return render_template(
            'profiles/profile.html', inputs=inputs, form_attr=form_attr, 
            note=note, desc=desc, right_btn_ref=right_btn_ref, left_btn_ref=left_btn_ref
        )
    elif data.status_code == 404:
        return request.url
    elif fetchd := data.json() and data.ok:
        return render_template(
            'profiles/profile.html', inputs=inputs, form_attr=form_attr, 
            data=fetchd, note=note, desc=desc, right_btn_ref=right_btn_ref, left_btn_ref=left_btn_ref
        ) 
    elif data.status_code == 401:
        return request.url
    

@prof.post("/basics")
def basics():

    post_data = json.dumps(request.form)
    data = ReqApi(req_typ="post", req_url=url_for("profa.basic"), post_data=post_data)
    data = data()
    
    if not data.ok:
        return data
    elif data.ok:
        return redirect(url_for('profs.prof.acadForm'))
    elif data.status_code == 404:
        return request.url
    return redirect(url_for('localhost:3000'))


@prof.get("/academics")
def acadForm():
    """user universal accedemic profile"""

    base_flds = ['Institution', 'Discipline', 'Title', 'Start', 'End']
    form_attr, inputs = form_dict(endpt=url_for("profs.prof.acadas"), fields=base_flds)
    left_btn_ref = "/profiles/app/basics"
    right_btn_ref = "/profiles/app/researchs"
    desc = "Accademic profile is subject to verification"

    data = ReqApi(req_typ="get", req_url=url_for("profa.accademics")+"?usr=true")
    data = data()

    if not request.values:
        return render_template('profiles/profile.html', inputs=inputs, form_attr=form_attr, desc=desc, right_btn_ref=right_btn_ref, left_btn_ref=left_btn_ref)
    elif data.status_code == 404:
        return request.url
    elif fetchd := data.json() and data.ok:
        return render_template('profiles/profile.html', inputs=inputs, form_attr=form_attr, data=fetchd, desc=desc, right_btn_ref=right_btn_ref, left_btn_ref=left_btn_ref)
    elif data.status_code == 401:
        return request.url
    

@prof.post("/accademics")
def acadas():

    acad = json.dumps(request.form)
    data = ReqApi(req_typ="post", req_url=url_for("profa.accademics"), post_data=acad)
    data = data()
    
    if not data.ok:
        return data
    elif data.status_code == 404:
        return request.url
    elif data.ok:
        return redirect(url_for("profs.prof.resrchForm"))
    return redirect(url_for("profs.prof.resrchForm"))

@prof.get("/researchs")
def resrchForm():

    base_flds = ['Institution', 'Discipline', 'Email', 'Type of Research', 'Start', 'End']
    form_attr, inputs = form_dict(endpt=url_for("profs.prof.resrcha"), fields=base_flds)
    note = {"org": "this could be an accademic research work", "emel": "This must be an organisation or institution email. It's subject to verification"}
    left_btn_ref = "/profiles/app/academics"
    right_btn_ref = "/profiles/app/works"
    desc = "fill up the profile below as a researcher with respect to organisation or institution of research"

    data = ReqApi(req_typ="get", req_url=url_for("profa.resacher")+"?usr=true")
    data = data()

    if not request.values:
        return render_template('profiles/profile.html', inputs=inputs, form_attr=form_attr, note=note, right_btn_ref=right_btn_ref, left_btn_ref=left_btn_ref, desc=desc)
    elif data.status_code == 404:
        return request.url
    if data := data.json() and data.ok:
        return render_template('profiles/profile.html', inputs=inputs, form_attr=form_attr, data=data, note=note, right_btn_ref=right_btn_ref, left_btn_ref=left_btn_ref, desc=desc)
    elif data.status_code == 404:
        return request.url

@prof.post("/researchs")
def resrcha():

    data = ReqApi(req_typ="post", req_url=url_for("profa.resacher"), post_data=json.dumps(request.form))
    data = data()

    if not data.ok:
        return data
    elif data.ok:
        return redirect(url_for('profs.prof.workForm'))
    elif data.status_code == 404:
        return request.url
    return redirect(url_for('profs.prof.resrchForm'))

@prof.get("/works")
def workForm():

    base_flds = ['Organisation', 'Role', 'Start', 'End']
    form_attr, inputs = form_dict(endpt=url_for("profs.prof.works"), fields=base_flds)
    left_btn_ref = "/profiles/app/researchs"
    right_btn_ref = '/profiles/app/profile'
    desc = "fill work experience in other to share and mentor, you take what you give"

    data = ReqApi(req_typ="get", req_url=url_for("profa.works")+"?usr=true")
    data = data()

    if not request.values:
        return render_template('profiles/profile.html', inputs=inputs, form_attr=form_attr, right_btn_ref=right_btn_ref, left_btn_ref=left_btn_ref, desc=desc)
    elif data.status_code == 404:
        return request.url
    if data := data.json() and data.ok:
        return render_template('profiles/profile.html', inputs=inputs, form_attr=form_attr, data=data, right_btn_ref=right_btn_ref, left_btn_ref=left_btn_ref, desc=desc)
    return data

@prof.post("works")
def works():

    data = ReqApi(req_typ="post", req_url=url_for("profa.works"), post_data=json.dumps(request.form))
    data = data()
    
    if not data.ok:
        return data
    elif data.ok:
        return redirect(url_for('grocs.groc.prof'))
    elif data.status_code == 404:
        return request.url
    return redirect(url_for('localhost'))
