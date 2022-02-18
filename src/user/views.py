
import tempfile
from werkzeug.utils import secure_filename
from asyncio import streams
import io
import json
import os

from werkzeug.datastructures import FileStorage
from flask import flash, render_template, redirect, url_for, Blueprint, request

from setting.helper import ReqApi, form_dict


grocs = Blueprint('groc', __name__, url_prefix="/user")


@grocs.post("award")
def cr8award():
    post_data = json.dumps(request.form)
    data = ReqApi(req_typ="post", req_url=url_for("groca.awards"), post_data=post_data)
    data = data()
    
    if data.is_redirect:
        return data
    if not data.ok:
        return data
    elif data.ok:
        redirect(url_for('groca.profiles'))
    redirect(url_for('localhost:3000'))

@grocs.get("award")
def awards():
    "user bsic knowledge profile"

    data = ReqApi(req_typ="get", req_url=url_for("groca.awards"))
    awd_flds = ['Place', 'Job', 'Award Title', 'Award Date']
    form_attr, inputs = form_dict(endpt="grocs.groc.cr8award", fields=awd_flds)
    
    desc = ""
    data = data()

    if data.is_redirect:
        return data
    if not data.ok:
        return data
    elif data := data.json():
        return render_template(
            'profiles/profile.html', inputs=inputs, form_attr=form_attr, data=data, desc=desc
        )
    return render_template(
        'profiles/profile.html', inputs=inputs, form_attr=form_attr, desc=desc
    )

@grocs.post("pubs")
def cr8pub():

    post_data = json.dumps(request.form)
    data = ReqApi(req_typ="post", req_url=url_for('groc.pubs'), post_data=post_data)
    data = data()

    if not data.ok:
        return data
    elif data.ok:
        redirect(url_for('grocs.groc.pubs'))
    redirect(url_for('localhost:3000'))

@grocs.get("pubs")
def pubs():
    """user universal accedemic profile"""
    # Institution will be selection of institutions as a researcher
    data = ReqApi(req_typ="get", req_url=url_for("groca.awards"))
    pub_flds = ['Institution', 'Field', 'Title', 'File', 'Publication Date']
    form_attr, inputs = form_dict(endpt="grocs.groc.cr8pub", fields=pub_flds)
    data = data()

    if data.is_redirect:
        return data
    if not data.ok:
        return data
    elif data := data.json():
        return render_template('profiles/pubs.html', inputs=inputs, form_attr=form_attr, data=data)
    return render_template('profiles/pubform.html', inputs=inputs, form_attr=form_attr)

@grocs.post("social")
def cr8hub():
    post_data = json.dumps(request.form)
    data = ReqApi(req_typ="post", req_url=url_for("groca.socs"), post_data=post_data)
    data = data()

    if data.is_redirect:
        return data
    if not data.ok:
        return data
    elif data.ok:
        redirect(url_for('groca.profiles'))
    redirect(url_for('localhost:3000'))

@grocs.get("social")
def hubs():
    # this still needs proper review and development
    data = ReqApi(req_typ="get", req_url=url_for("groca.socs"))
    soc_flds = ['Hubby title', 'type of hubby']
    form_attr, inputs = form_dict(endpt="grocs.groc.hubs", fields=soc_flds)
    data = data()

    if data.is_redirect:
        return data
    if not data.ok:
        return data
    elif data := data.json():
        return render_template('profiles/profile.html', inputs=inputs, form_attr=form_attr, data=data)
    return render_template('profiles/soc.html', inputs=inputs, form_attr=form_attr)

@grocs.post("pix")
def cr8pix():
    req_file = request.files["file"]
    
    if req_file.filename:
        fn = os.path.basename(req_file.filename)
    #tmp_file = tempfile.NamedTemporaryFile()
    #file = tmp_file.write(io.FileIO(file))
    #file = req_file['file']
    #file.filename = secure_filename(file.filename) 
    #file = file.save
    with open(file=fn, mode="wb") as upload:
        upload = upload.write(req_file.stream.read())
        print(upload)
        data = ReqApi(req_typ="post", req_url=url_for("groca.avatars"), file={"file": upload})
    data = data()

    print(data)
    if data.is_redirect:
        return data
    if not data.ok:
        return data
    elif data.ok:
        return redirect(url_for('grocs.groc.pix'))
    return redirect(request.url)

@grocs.get("pix")
def pixs():
    pix = ReqApi(req_typ="get", req_url=url_for("groca.avatars"))
    if pix := pix() is not None:
        pix = pix.json()
    pix = None

    return render_template('profiles/pix.html', usr_pix=pix)

@grocs.get("profile")
def prof():
    
    data = ReqApi(req_typ="get", req_url=url_for("groca.profiles"))
    return render_template('profiles/profile.html', data=data)



# this is for spotlight and services
@grocs.post("mindme")
def cr8minda():

    post_data = json.dumps(request.form)
    data = ReqApi(req_typ="post", req_url=url_for("groca.awards"), post_data=post_data)
    data = data()

    if data.is_redirect:
        return data
    if not data.ok:
        return data
    elif data.ok:
        flash(message="Reminder has been set successfully")
        redirect(url_for('localhost:3000'))

@grocs.get("mindme")
def minda():

    data = ReqApi(req_typ="get", req_url=url_for("groca.awards"))
    rmind_flds = ['Location', 'Field', 'Knowledge', 'Start', 'End']
    form_attr, inputs = form_dict(endpt="profs.prof.basics", fields=rmind_flds)
    data = data()

    if data.is_redirect:
        return data
    if not data.ok:
        return data
    elif data := data.json():
        return render_template('profiles/reminda.html', data=data)
    return render_template('profiles/profile.html', inputs=inputs, form_attr=form_attr)