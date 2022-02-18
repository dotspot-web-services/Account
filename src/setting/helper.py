
import os
import requests
import json

from flask import redirect, flash, session
from werkzeug.utils import secure_filename

from .base.setting import CheckSet



def form_dict(endpt, fields) -> dict:
    """[summary]

    Args:
        endpt ([type]): [description]

    Returns:
        [type]: [description]
    """
    inputs = {}
    form_attr = {
        "method": "POST", "action": f"{CheckSet().dormain+endpt}", "id": "proForm",
        "button": { "class": "btn btn-block btn-success my-2 my-sm-0", "value": "Submit"}
    }
    allinput = {
        'Contact': {"type": "text", "name": "cont", "class": "form-control", "placeholder": "Enter your contact"},
        'Email': {'placeholder': 'organisation or institution email', "type": "email", "name": "emel"},
        'Discipline': {'placeholder': 'Enter Course of study', "type": "text", "name": "dspln"}, 
        'Institution': {'value': '', 'placeholder': 'Enter Institution name', "type": "text", "name": "plc"},
        'Organisation': {'placeholder': 'Organisation or institution', "type": "text", "name": "plc"},
        'Class': {'placeholder': 'Field of knowledge. eg: fashion, sciences, football, arts', "type": "text", "name": "dspln"}, 
        'Location': {'placeholder': 'name of the place', "type": "text", "name": "plc"},
        'Role': {'placeholder': 'name of the place', "type": "text", "name": "dspln"},
        'Knowledge': {"labels":{'Unskilled': {'value': 0}, 'Skilled': {'value': 1}}, "type": "radio", "name": 'typ'},
        'Field': {'placeholder': 'Area of Research', "type": "text", "name": "dspln"},
        'Type of Research': {"labels":{'Organisation': {'value': True}, 'Accademic': {'value': False}}, "type": "typ", "name": 'radio'},
        'Title': {"options": {'degree':'First Degree', 'certified': 'Certification', 'masters':'Masters Degree', 'doctor':'Doctorate Degree', 'NCE':'NCE', 'OND':'OND', 'HND':'HND'}, "type": "select", "name": "ttl"},
        'Start': {'placeholder': 'year', "name": "strt", "type": "number",}, 'End': {'placeholder': 'year', "name": "end", "type": "number",},
    }

    inputs = {key: allinput[key] for key in fields  if key in allinput.keys()}
    
    return form_attr, inputs

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
    def __init__(self, req_typ, req_url, post_data=None, file=None) -> None:
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
        self.__dmain = CheckSet().dormain
        self.header = {"Content-type": "application/json; charset=UTF-8", "Authorization": session.get('token', None)}
        
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
                    print("its working...")
                    print(self.file)
                    req = requests.post(url=self.__dmain+self.addr, files=self.file, headers=self.header)
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
        self.file = file
        self.filename = self.file.filename

    def allowed_type(self):
        """check if the file type is allowed and return boolean value
        """
        if not "." in self.filename:
            return False
        if not self.filename.rsplit(".", 1)[1] in CheckSet.allowed_extension:
            return False
        return secure_filename(self.filename)

    def save_file(self):
        """save file and return path
        """
        if not (checked := self.allowed_type()):
            return
        return self.file.save(os.path.join(CheckSet.media_folder), checked)

    def __call__(self, *args: int) -> str:
        if self.filename == "" and self.allowed_type():
            return "invalid file"


if __name__ == "__main__":
    form = {"fn": "john mba", "cont": "nwanjamba@gmail.com", "pwd": "nalkjiofcji98", "vpwd": "nalkjiofcji98"}
    pg = ReqApi(req_typ="post", req_url=CheckSet().dormain+"/accounts/api/reg", post_data=form)
