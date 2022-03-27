
import json

from werkzeug.datastructures import ImmutableMultiDict
from flask import flash, render_template, redirect, url_for, Blueprint, request

from setting.helper import ReqApi, form_dict


grocs = Blueprint('groc', __name__, url_prefix="/user")


@grocs.get("welcome")
def wlcm():
    
    return render_template('pages/wlc.html')

@grocs.post("award")
def cr8award():
    post_data = json.dumps(request.form)
    data = ReqApi(req_typ="post", req_url=url_for("groca.awards"), post_data=post_data)
    data = data()
    
    if not data.ok:
        return data
    elif data.ok:
        redirect(url_for('groca.profiles'))
    elif data.status_code == 404:
        return request.url
    redirect(url_for('localhost:3000'))

@grocs.get("award")
def awards():
    "user bsic knowledge profile"

    data = ReqApi(req_typ="get", req_url=url_for("groca.awards")+"?usr=true")
    awd_flds = ['Place', 'Job', 'Award Title', 'Award Date']
    form_attr, inputs = form_dict(endpt=url_for("grocs.groc.cr8award"), fields=awd_flds)
    
    desc = ""
    resp = data()

    if not request.values :
        return render_template(
            'profiles/profile.html', inputs=inputs, form_attr=form_attr, desc=desc
        )
    elif resp.status_code == 404:
        return request.url
    elif (data := data.json()) and resp.ok:
        return render_template(
            'profiles/profile.html', inputs=inputs, form_attr=form_attr, data=data, desc=desc
        )
    return resp

@grocs.post("pubs")
def cr8pub():

    post_data = json.dumps(request.form)
    data = ReqApi(req_typ="post", req_url=url_for('groc.pubs'), post_data=post_data)
    data = data()

    if not data.ok:
        return data
    elif data.ok:
        redirect(url_for('grocs.groc.pubs'))
    elif data.status_code == 404:
        return request.url
    redirect(url_for('localhost:3000'))

@grocs.get("pubs")
def pubs():
    """user universal accedemic profile"""
    # Institution will be selection of institutions as a researcher
    data = ReqApi(req_typ="get", req_url=url_for("groca.awards")+"?usr=true")
    pub_flds = ['Institution', 'Field', 'Title', 'File', 'Publication Date']
    form_attr, inputs = form_dict(endpt=url_for("grocs.groc.cr8pub"), fields=pub_flds)
    resp = data()

    if request.values:
        return render_template('profiles/pubform.html', inputs=inputs, form_attr=form_attr)
    elif resp.status_code == 404:
        return request.url
    if (data := resp.json()) and resp.ok:
        return render_template('profiles/pubs.html', inputs=inputs, form_attr=form_attr, data=data)
    return resp

@grocs.post("social")
def cr8hub():
    post_data = json.dumps(request.form)
    data = ReqApi(req_typ="post", req_url=url_for("groca.socs"), post_data=post_data)
    data = data()

    if not data.ok:
        return data
    elif data.ok:
        redirect(url_for('groca.profiles'))
    elif data.status_code == 404:
        return request.url
    redirect(url_for('localhost:3000'))

@grocs.get("social")
def hubs():
    # this still needs proper review and development
    data = ReqApi(req_typ="get", req_url=url_for("groca.socs"))
    soc_flds = ['Hubby title', 'type of hubby']
    form_attr, inputs = form_dict(endpt=url_for("grocs.groc.hubs"), fields=soc_flds)
    resp = data()

    if request.values:
        return render_template('profiles/soc.html', inputs=inputs, form_attr=form_attr)
    elif resp.status_code == 404:
        return request.url
    elif (data := resp.json()) and resp.ok:
        return render_template('profiles/profile.html', inputs=inputs, form_attr=form_attr, data=data)
    return data
    
@grocs.post("pix")
def cr8pix():

    req_file = request.files
    file = ImmutableMultiDict([("file", req_file.get("file"))])
    data = ReqApi(req_typ="post", req_url=url_for("groca.avatars"), file=file)

    data = data()

    print(file)
    if not data.ok:
        return data
    elif data.ok:
        return redirect(url_for('grocs.groc.pixs'))
    elif data.status_code == 404:
        return request.url
    return redirect(request.url)

@grocs.get("pix")
def pixs():

    pix = ReqApi(req_typ="get", req_url=url_for("groca.avatars"))
    resp = pix()
    
    if (pix := resp.json()) and resp.ok:
        if not isinstance(pix, dict):
            print("that is the pix")
            return render_template('profiles/pix.html', usr_pix=pix)
    return render_template('profiles/pix.html', usr_pix=None)

@grocs.get("profile")
def prof():
    
    data = ReqApi(req_typ="get", req_url=url_for("groca.profiles"))
    resp =data()
    
    if resp.status_code == 404:
        return request.url
    if (data := resp.json()) and resp.ok:
        return render_template('pages/profile.html', data=data.get("json_build_object"))
    return resp


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
    resp = data()

    if request.values:
        return render_template('profiles/profile.html', inputs=inputs, form_attr=form_attr)
    elif resp.is_redirect:
        return data
    elif (data := resp.json()) and resp.ok:
        return render_template('profiles/reminda.html', data=data)
    return data

