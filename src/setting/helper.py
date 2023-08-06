
import os
import smtplib
from typing import Any
from dns.resolver import query
import shutil
import requests

from flask import redirect, flash, session, url_for, render_template, request
from werkzeug.utils import secure_filename

from .base.setting import CheckSet


def verifymail(dormain, host, mail):
        
    server = smtplib.SMTP()
    records = query(dormain, 'MX')
    mxRecord = records[0].exchange
    if mxRecord:
        return
    mxRecord = str(mxRecord)
    # SMTP lib setup (use debug level for full output)
    server.set_debuglevel(0)
    # SMTP Conversation
    server.connect(mxRecord)
    server.helo(server.local_hostname) ### server.local_hostname(Get local server hostname)
    server.mail(host)
    code, message = server.rcpt(str(mail))
    server.quit()
    if code == 250: # Assume SMTP response 250 is success
        print('Success')
    else:
        print("Bad")
        print(code)
        print(message)

def downloader(url, directory, fname=None):
    """_summary_

    Args:
        url (_type_): _description_
        directory (_type_): _description_
        fname (_type_, optional): _description_. Defaults to None.
    """
    if fname == None:
        fname = os.path.basename(url)
    dl_path = os.path.join(directory, fname)
    with requests.get(url, stream=True) as r:
        with open(dl_path, "wb") as f:
            shutil.copy(src=r.raw, dst=f)
    return dl_path

def handle_ui_response(status, data, flas=""):
    """_summary_

    Args:
        status (_type_): _description_
        data (_type_): _description_
        flas (str, optional): _description_. Defaults to "".
    """

    if status == 200:
        session["active"] = False
        session["token"] = data
        return redirect(url_for('accs.regs.finalize'))
    elif status == 422:
        return render_template('/registry/reg.html', endpt=url_for('accs.regs.regPage'), fields="register", data=data)
    elif status == 409:
        flash(message="Account already exists, please login", category="info")
        return  redirect(request.url)

def convert_errors(err):
    """_summary_

    Args:
        err (_type_): _description_

    Raises:
        Exception: _description_

    Returns:
        _type_: _description_
    """
    
    error = {}
    for item in err.errors():
        error[item.get("loc")[0]] = item.get("msg")
    return error
    
class FormData:
    
    def __init__(self, endpt:str, form_fields:dict or str, **extras:dict) -> None:
        """Generate for inputs and attributes for instructing jinja templating

        Args:
            endpt (str): url endpoint to process form
            fields (dict, optional): name and label pair of form input. Defaults to {}.
            registry (str, optional): either login, register, contact, email or number. Defaults to ''.
        """
        self.fields = form_fields
        self.extras = extras
        self.endpt = endpt
        default_form = ["contact", "recover", "register", "login", "work", "research", "accademic", "basic", "award", "social"]
        
        if isinstance(self.fields, str):
            self._registry = True
            self.fields = self.fields.lower()
        if self.fields not in default_form and not isinstance(self.fields,  dict):
            raise Exception("fieldsError: Fields can either be default form or input fields")
        if self.fields in default_form[0 : 4]:
            self.fields, self.extras = self.regData(value=self.fields)
        if  self.fields in  default_form[5 : -3]:
            self.fields, self.extras = self.profData(value=self.fields)
        if  self.fields in  default_form[-2 : -1]:
            self.fields, self.extras = self.usrData(value=self.fields)
        self.prof = {
            'emel':'Email', 'displn': 'Discipline', 'plc': 'Institution', 'org':'Organisation', 'cls': 'Class',
            'locatn':'Location', 'rol':'Role', 'knwlg':'Knowledge', 'fld':'Field', 'resech':'Type of Research',
            'ttl':'Title', 'strt':'Start', 'end':'End'
        }
        inputs = {
            'Contact': {"type": "text", "name": "cont", "class": "form-control", "placeholder": "Enter your contact"},
            'Email': {'placeholder': 'organisation or institution email', "type": "email", "name": "emel"},
            'Discipline': {'placeholder': 'Enter Course of study', "type": "text", "name": "displn"}, 
            'Institution': {'value': '', 'placeholder': 'Enter Institution name', "type": "text", "name": "plc"},
            'Organisation': {'placeholder': 'Organisation or institution', "type": "text", "name": "org"},
            'Class': {'placeholder': 'Field of knowledge. eg: fashion, sciences, football, arts', "type": "text", "name": "cls"}, 
            'Location': {'placeholder': 'name of the place', "type": "text", "name": "locatn"},
            'Role': {'placeholder': 'name of the place', "type": "text", "name": "dspln"},
            'Knowledge': {"labels":{'Unskilled': {'value': 0}, 'Skilled': {'value': 1}}, "type": "radio", "name": 'knwlg'},
            'Field': {'placeholder': 'Area of Research', "type": "text", "name": "fld"},
            'Type of Research': {"labels":{'Organisation': {'value': 1}, 'Accademic': {'value': 0}}, "type": "radio", "name": 'resrch'},
            'Title': {"options": {'degree':'First Degree', 'certified': 'Certification', 'masters':'Masters Degree', 'doctor':'Doctorate Degree', 'NCE':'NCE', 'OND':'OND', 'HND':'HND'}, "type": "select", "name": "ttl"},
            'Start': {'placeholder': 'year', "name": "strt", "type": "number",}, 'End': {'placeholder': 'year', "name": "end", "type": "number",},
        }
    
    def form(self):
        form_attr = {"action": f"{self.endpt}"}
        form_attr["method"] = self.extras.get("method", "POST")
        form_attr[ "button"] = self.extras.get('button', {"label": "Create"})
        return form_attr
    
    def regData(self, value:str):
        """Generate registeration data
        """
        regInp = {
            'fname':"Full Name", 'cont':"Contact", 'pwd':'password', 'pwd2':'Confirm password',
            'tnc':'I accept the {}, {} and {} of this site.'
        }
        fields = ""
        extras = {}
        
        if  value.lower() == "login":
            fields = {'cont': regInp["cont"], 'pwd': regInp['pwd']}
            extras = {
                'pwd': {"note": {"a": {"Reset password":"/accounts/app/contact"}},"type":"password"}, 'button':{"label":"Login"}
            }
        elif value.lower() == "register":
            fields = regInp
            extras = {'tnc':{"type":"checkbox", "label": {"a": (
                    {"Terms":"tnc.html"}, {"Conditions":"tnc.html"}, {"privacy policy": "tnc.html"}
                )}},'pwd': {"type":"password"}, 'pwd2': {"type":"password"}, 'fn':{'placeholder': 'Seperate names with space'}}
        elif value.lower() == "recover":
            fields = {'pwd': regInp["pwd"], 'pwd2': regInp["pwd2"]}
            extras = {'button':{"label":"Reset"},
                'pwd': {"type":"password"}, 'pwd2':{"placeholder":"Confirm password", "type":"password"}}
        elif value.lower() == "contact":
            fields = {'cont': regInp["cont"]}
            extras = {
                'cont':{"placeholder":"Enter the email or phone number used in registeration"}, 'button': {"label":"Submit"}}
        elif value.lower() == "email":
            fields = {"emel": "Email"}
        return fields, extras
    
    def profData(self, value:str):
        
        plc = {'locatn':'Institution', 'fld':'Field', 'edu':'Knowledge'}
        duratn = {'strt':'Start', 'end':'End'}
        fields = ""
        extras = {}
        
        if value.lower() == "basic":
            plc['locatn'] = 'Location'
            plc.update(duratn)
            fields = plc
            extras = {'fld':{'placeholder': 'E.g an accademy, sciences, arts'}}
        elif value.lower() == "accademic":
            plc['spec'] = 'Specialization'
            plc['ttl'] = 'Title'
            plc.update(duratn)
            fields = plc
            extras = {'ttl':{"type":"search"}}
        elif value.lower() == "research":
            plc['emel'] = 'Email'
            plc['typ'] = 'Type of Research'
            plc.update(duratn)
            fields = plc
            extras = {
                'emel':{'placeholder': 'organisation or institution email', "type": "email"}
            }
        elif value.lower() == "work":
            fields = {'org': 'Organisation', 'rol': 'Role'}
            plc.update(duratn)
            fields = plc
            extras = {'rol':{'placeholder': 'The job rol or position'}}
        return fields, extras
    
    def usrData(self, value):
        if value.lower() == "award":
            fields = {'titl': 'Organisation', 'typ': 'Role'}
            extras = {'rol':{'placeholder': 'The job rol or position'}}
        elif value.lower() == "social":
            fields = {'plc': 'Organisation', 'acts': 'Role', "ttl": "Title", "awdt": "Date"} 
            extras = {'rol':{'placeholder': 'The job rol or position'}}
        return fields, extras
        
    def geninp(self, name):
        """ Check if theres an extra configs for an input with the name and
        Generate and return an input for the form

        Args:
            name (str): Name of an input with extras used as key in extras
            typ (string): _description_
            label (strin): _description_
        """
        
        inpt = {}
        extattr = self.extras.get(name)

        if extattr:
            inpt.update(extattr)
        if self._registry and name != "end":
            inpt["required"] = "required"
        inpt['name'] = name
        return inpt

    def form_dict(self) -> dict:
        """[summary]

        Args:
            endpt ([type]): [description]

        Returns: 
            [type]: [description]
        """
        
        inputs = {val:self.geninp(name=key) for key, val in self.fields.items()}
        return self.form(), inputs
    
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.form_dict()


if __name__ == "__main__":
    #form = {"fn": "john mba", "cont": "nwanjamba@gmail.com", "pwd": "nalkjiofcji98", "vpwd": "nalkjiofcji98"}
    #pg = ReqApi(req_typ="post", req_url=CheckSet().dormain+"/accounts/api/reg", post_data=form)
    def_form = FormData(endpt="url_for('accs.regs.regPage')", form_fields='contact')()
    print(def_form)
