
from flask import render_template, wrappers

from setting.decs import Auths as authenticate
from setting.dbcon import DbSet


@authenticate
def basics(usr):
    db = DbSet()
    if isinstance(usr, wrappers.Response):
        return usr
    with db.get_db() as con:
        basic = db._model.basic_prof(
            con, usr=usr
        )
    
    form_attr = {
        "method": "POST", "action": "/src", "class": "form-inline my-2 my-lg-0",
        "button": { "class": "btn btn-outline-success my-2 my-sm-0", "label": "Search"}
    }
    inputs = {
        'discipline': {'placeholder': 'Field of knowledge', "type": "text", "name": "dspln"}, 
        'place': {'placeholder': 'name of the place', "type": "text", "name": "plc"}, 'Skilled': {'value': 0},
        'started': {'type': 'number', 'name': 'strt'}, 'Ended': {'type': 'number', 'name': 'endd'}
    }
    
    if basic :
        return render_template('pages/profile.html', inputs=inputs, form_attr=form_attr, data=basic)
    return render_template('pages/profile.html', inputs=inputs, form_attr=form_attr)

@authenticate
def acadas(usr):
    """reset password"""
    db = DbSet()
    if isinstance(usr, wrappers.Response):
        return usr

    with db.get_db() as con:
        acad = db._model.acads_prof(
            con, usr=usr
        )

    form_attr = {
        "method": "POST", "action": "/src", "class": "form-inline my-2 my-lg-0",
        "button": { "class": "btn btn-outline-success my-2 my-sm-0", "label": "Search"}
    }
    inputs = {
        'discipline': {'value': '', 'placeholder': 'Enter Course of study'}, 'place': {'value': '', 'placeholder': 'Enter Institution name'}, 
        'title': {"options": ['B.Sc', 'B.Engr' 'M.Sc', 'Ph.Dr'], "type": "select", "name": "ttl"}, 'started': {'placeholder': 'year'}, 'Ended': {'placeholder': 'year'}
    }
    if acad :
        return render_template('pages/profile.html', inputs=inputs, form_attr=form_attr, data=acad)
    return render_template('pages/profile.html', inputs=inputs, form_attr=form_attr)


@authenticate
def resrcha(usr):
    db = DbSet()
    if isinstance(usr, wrappers.Response):
        return usr

    with db.get_db() as con:
        srcha = db._model.rsrch_prof(
            con, usr=usr
        )

    form_attr = {
        "method": "POST", "action": "/src", "class": "form-inline my-2 my-lg-0",
        "button": { "class": "btn btn-outline-success my-2 my-sm-0", "label": "Search"}
    }
    inputs = {
        'type': {'value': ''}, 'organisation': {'value': ''},
        'started': {'type': 'date'}, 'Ended': {'value': 1}, 'email': {'value': 0}
    }

    if srcha :
        return render_template('pages/profile.html', inputs=inputs, form_attr=form_attr, data=srcha)
    return render_template('pages/profile.html', inputs=inputs, form_attr=form_attr)

def works(usr):
    db = DbSet()
    if isinstance(usr, wrappers.Response):
        return usr
        
    with db.get_db() as con:
        wrk = db._model.wk_prof(
            con, usr=usr
        )

    form_attr = {
        "method": "POST", "action": "/src", "class": "form-inline my-2 my-lg-0",
        "button": { "class": "btn btn-outline-success my-2 my-sm-0", "label": "Search"}
    }
    inputs = {
        'organisation': {'value': ''}, 'role': {'value': ''},
        'started': {'type': 'date'}, 'Ended': {'value': 1}
    }

    if wrk :
        return render_template('pages/profile.html', inputs=inputs, form_attr=form_attr, data=wrk)
    return render_template('pages/profile.html', inputs=inputs, form_attr=form_attr)
    