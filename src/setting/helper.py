
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


class Responder(object):

    def __init__(self, status_code, data=None) -> None:
        """decorator for examining and returning appropriate response

        Args:
            status_code (int): http status response code
            data (dict or string, optional): dict if data is feched but string when reporting an error. Defaults to None.
        """
        self.status = status_code
        self.data = data

    def message(self):
        """return an http response code determined message

        Returns:
            dict: dictionary response message
        """
        msg = {"message": "operation is successful"}
        
        if self.status == 200:
            return
        if self.status == 201:
            return msg
        if self.status == 401 and self.data is None:
            msg["message"] = "Unauthorized operation"
            return msg
        if self.status == 409 and self.data is None:
            msg["message"] = "Duplicate data operation"
            return msg
        if self.status == 422 and self.data is not None:
            return

    def response(self):
        """return an http response code and data or message as determined data

        Returns:
            dict: dictionary response message or data
        """
        if msg := self.message() and msg is None:
            return self.status, self.data
        elif self.data is None:
            return self.status, msg

def ApiResp(status_code, data=None):
    """data and status_code determine the response message

    Args:
        status_code (int): API response code
        data (dict): API response data
    """
    if data is None :
        return status_code
    elif data is not None:
        return data, status_code

class ReqApi:
    """generate a request header based on the type of request
    """
    def __init__(self, req_typ, req_url, post_data=None, file=None, auth=True) -> None:
        """[summary]

        Args:
            req_typ (string): the type of request to be done
            req_url (url): the request destination url
            post_data (dict): post data if making a post request
        """
        self.addr = req_url
        self.reqst = req_typ
        self.data = post_data
        self.file = file
        self.aut = auth
        self.__dmain = CheckSet().dormain
        self.header = self.setheader()

    def setheader(self):
        if self.file is None:
            cntyp = "application/json"
        else:
            cntyp = "multipart/form-data"
        if session and self.aut:
            return {
                "Content-type": f"{cntyp}; charset=UTF-8", "Authorization": session.get("token", None)
            }
        return {
                "Content-type": f"{cntyp}"
            }
        

    def auth(self):
        if isinstance(self.data, tuple):
            auth = self.data
            return auth

    def req(self):
        """make a request to the class url
        """
        match self.reqst:
            case "post":
                if auth := self.auth():
                    req = requests.post(url=self.__dmain+self.addr, data={}, headers=self.header, auth=auth)
                elif self.file and self.data is not None:
                    req = requests.post(url=self.__dmain+self.addr, data=self.data, files=self.file, headers=self.header)
                elif self.file is not None:
                    print(self.file)
                    req = requests.post(url=self.__dmain+self.addr, data=self.file, headers=self.header, verify=True)
                    print(req.text)
                elif self.data is not None:
                    req = requests.post(url=self.__dmain+self.addr, data=self.data, headers=self.header)
            case "get":
                req = requests.get(url=self.__dmain+self.addr, headers=self.header)
            case "put":
                if self.file and self.data is not None:
                    req = requests.put(url=self.__dmain+self.addr, data=self.data, files=self.file, headers=self.header)
                elif self.file is not None:
                    req = requests.put(url=self.__dmain+self.addr, files=self.file, headers=self.header)
                elif self.data is not None:
                    req = requests.put(url=self.__dmain+self.addr, data=self.data, headers=self.header)
        return req

    def failed(self, status: int):
        """use http status code to verify if the request and redirect to home page or false

        Args:
            status (int): http response status code

        Returns:
            {'status': 'failed', 'message': 'invalid form values'}
            {'status': 'failed', 'message': 'user already exist'}
            [type]: returns a redirect or false
        """
        if status == 401:
            flash(message="You are not logged in or session has expired", category="info")
            return redirect(self.__dmain)
        if status > 401:
            flash(message="An error occured, try again later", category="error")
            return redirect("localhost")

    def status(self):
        """make a request to the class url
        """
        if (req:= self.req()) and req.ok:
            return req
        else:
            return self.failed(status=req.status_code)
    
    def __call__(self):
        if req:=self.status():
            return req


class FileUp:
    """do file checks, save and return filepath.
    """
    def __init__(self, file) -> None:
        self.setup = CheckSet()
        self.file = file
        self.filename = self.file.filename

    def allowed_type(self):
        """check if the file type is allowed and return boolean value
        """
        if not "." in self.filename:
            return False
        if not self.filename.rsplit(".", 1)[1] in self.setup.allowed_extension:
            return False
        return secure_filename(self.filename)

    def save_file(self):
        """save file and return path
        """
        if not (checked := self.allowed_type()):
            return
        return self.file.save(os.path.join(self.setup.media_folder), checked)

    def __call__(self, *args: int) -> str:
        if self.filename == "" and self.allowed_type():
            return "invalid file"
        print(self.save_file())
        return self.save_file()


if __name__ == "__main__":
    #form = {"fn": "john mba", "cont": "nwanjamba@gmail.com", "pwd": "nalkjiofcji98", "vpwd": "nalkjiofcji98"}
    #pg = ReqApi(req_typ="post", req_url=CheckSet().dormain+"/accounts/api/reg", post_data=form)
    def_form = FormData(endpt="url_for('accs.regs.regPage')", form_fields='contact')()
    print(def_form)
