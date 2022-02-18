
import json

from flask import render_template, url_for, redirect, Blueprint, request

from setting.helper import ReqApi, form_dict


prof = Blueprint('prof', __name__, url_prefix="/profile")


dormain = "http://127.0.0.1:3000/"


@prof.get("/basics")
def basicForm():
    "user bsic knowledge profile"

    data = ReqApi(req_typ="get", req_url="profa.basic")
    base_flds = ['Location', 'Field', 'Knowledge', 'Start', 'End']
    form_attr, inputs = form_dict(endpt="profs.prof.basics", fields=base_flds)
    note = {"radio": "choose skilled if it's gotten in school and unskilled if not", 
        "dspln": "<div><span>skilled</span> could be any non universial tertiary education grouping of knowledge</div> <div><span>unskilled</span> could be from an accademy grouping of knowledge</div>",
        "class": "note"
    }
    left_btn_ref = "/accounts/account/app/registry/signIn"
    right_btn_ref = "/profiles/app/academics"
    desc = ""
    
    data = data()

    if data.is_redirect:
        return data
    if not data.ok:
        return data
    elif data := data.json():
        return render_template(
            'profiles/profile.html', inputs=inputs, form_attr=form_attr, 
            data=data, note=note, desc=desc, right_btn_ref=right_btn_ref, left_btn_ref=left_btn_ref
        )
    return render_template(
        'profiles/profile.html', inputs=inputs, form_attr=form_attr, 
        note=note, desc=desc, right_btn_ref=right_btn_ref, left_btn_ref=left_btn_ref
    )

@prof.post("/basics")
def basics():

    post_data = json.dumps(request.form)
    data = ReqApi(req_typ="post", req_url="profa.accademics", post_data=post_data)
    data = data()
    
    if data.is_redirect:
        return data
    if not data.ok:
        return data
    elif data.ok:
        return redirect(url_for('profs.prof.acadForm'))
    return redirect(url_for('localhost:3000'))


@prof.get("/academics")
def acadForm():
    """user universal accedemic profile"""

    data = ReqApi(req_typ="get", req_url="profa.accademics")
    base_flds = ['Institution', 'Discipline', 'Title', 'Start', 'End']
    form_attr, inputs = form_dict(endpt="profa.accademics", fields=base_flds)
    left_btn_ref = "/profiles/app/basics"
    right_btn_ref = "/profiles/app/researchs"
    desc = "Accademic profile is subject to verification"

    data = data()

    if data.is_redirect:
        return data
    if not data.ok:
        return data
    elif data := data.json():
        return render_template('profiles/profile.html', inputs=inputs, form_attr=form_attr, data=data, desc=desc, right_btn_ref=right_btn_ref, left_btn_ref=left_btn_ref)
    return render_template('profiles/profile.html', inputs=inputs, form_attr=form_attr, desc=desc, right_btn_ref=right_btn_ref, left_btn_ref=left_btn_ref)

@prof.post("/accademics")
def acadas():

    data = ReqApi(req_typ="post", req_url="profa.accademics")
    data = data()
    
    if data.is_redirect:
        return data
    if not data.ok:
        return data
    elif data.ok:
        return redirect(url_for('localhost'))
    return render_template('registry/finalReg.html', data=data[0])

@prof.get("/researchs")
def resrchForm():

    data = ReqApi(req_typ="get", req_url="profa.resacher")
    base_flds = ['Institution', 'Discipline', 'Email', 'Type of Research', 'Start', 'End']
    form_attr, inputs = form_dict(endpt="/profiles/api/Researcher", fields=base_flds)
    note = {"org": "this could be an accademic research work", "emel": "This must be an organisation or institution email. It's subject to verification"}
    left_btn_ref = "/profiles/app/academics"
    right_btn_ref = "/profiles/app/works"
    desc = "fill up the profile below as a researcher with respect to organisation or institution of research"

    data = data()

    if data.is_redirect:
        return data
    if not data.ok:
        return data
    elif data := data.json():
        return render_template('profiles/profile.html', inputs=inputs, form_attr=form_attr, data=data, note=note, right_btn_ref=right_btn_ref, left_btn_ref=left_btn_ref, desc=desc)
    return render_template('profiles/profile.html', inputs=inputs, form_attr=form_attr, note=note, right_btn_ref=right_btn_ref, left_btn_ref=left_btn_ref, desc=desc)

@prof.post("/researchs")
def resrcha():

    data = ReqApi(req_typ="post", req_url="profa.resacher")
    data = data()
    
    if data.is_redirect:
        return data
    if not data.ok:
        return data
    elif data.ok:
        return redirect(url_for('profs.prof.workForm'))
    return redirect(url_for('localhost'))

@prof.get("/works")
def workForm():

    data = ReqApi(req_typ="get", req_url="profa.works")
    base_flds = ['Organisation', 'Role', 'Start', 'End']
    form_attr, inputs = form_dict(endpt="/Profilers/Researcher", fields=base_flds)
    left_btn_ref = "/profiles/app/researchs"
    right_btn_ref = '/profiles/app/profile'
    desc = "fill work experience in other to share and mentor, you take what you give"

    data = data()

    if data.is_redirect:
        return data
    if not data.ok:
        return data
    elif data := data.json():
        return render_template('profiles/profile.html', inputs=inputs, form_attr=form_attr, data=data, right_btn_ref=right_btn_ref, left_btn_ref=left_btn_ref, desc=desc)
    return render_template('profiles/profile.html', inputs=inputs, form_attr=form_attr, right_btn_ref=right_btn_ref, left_btn_ref=left_btn_ref, desc=desc)

@prof.post("works")
def works():
    data = ReqApi(req_typ="get", req_url="profa.works")
    data = data()
    
    if data.is_redirect:
        return data
    if not data.ok:
        return data
    elif data.ok:
        return redirect(url_for('http://127.0.0.1:5000/Arenz'))
    return redirect(url_for('localhost'))


@prof.get("profile")
async def profile():
    data = ReqApi(req_typ="get", req_url=".accs.regApi.reg")

    data = data()

    if data.is_redirect:
        return data
    if not data.ok:
        return data
    elif data := data.json():
        return render_template('pages/profile.html', data=data)
    