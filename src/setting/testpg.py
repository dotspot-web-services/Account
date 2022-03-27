
import requests, json
from flask import redirect, flash
from base.setting import CheckSet


import re
import smtplib
import dns.resolver

# Address used for SMTP MAIL FROM command  
fromAddress = 'corn@bt.com'

# Simple Regex for syntax checking
regex = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,})$'

# Email address to verify
inputAddress = input('Please enter the emailAddress to verify:')
addressToVerify = str(inputAddress)

# Syntax check
match = re.match(regex, addressToVerify)
if match == None:
	print('Bad Syntax')
	raise ValueError('Bad Syntax')

# Get domain for DNS lookup
splitAddress = addressToVerify.split('@')
domain = str(splitAddress[1])
print('Domain:', domain)

# MX record lookup
records = dns.resolver.resolve(domain, 'MX')
print(records[0])
mxRecord = records[0].exchange
mxRecord = str(mxRecord)


# SMTP lib setup (use debug level for full output)
server = smtplib.SMTP()
server.set_debuglevel(0)

# SMTP Conversation
server.connect(mxRecord)
server.helo(server.local_hostname) ### server.local_hostname(Get local server hostname)
server.mail(fromAddress)
code, message = server.rcpt(str(addressToVerify))
server.quit()

print(code)
print(message)

# Assume SMTP response 250 is success
if code == 250:
	print('Success')
else:
	print('Bad')

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

class ReqApi(object):
    """generate a request header based on the type of request
    """
    def __init__(self, req_typ, req_url, post_data=None) -> None:
        """[summary]

        Args:
            req_typ (string): the type of request to be done
            req_url (url): the request destination url
            post_data (dict): post data if making a post request
        """
        self.addr = req_url
        self.reqst = req_typ
        self.data = post_data
        self.__dmain = "http://127.0.0.1:3000"
        self.header = {
            "Content-type": "application/json; charset=UTF-8"
        }

    def req(self):
        """make a request to the class url
        """
        match self.reqst:
            case "post":
                req = requests.post(url=self.__dmain+self.addr, data=self.data, headers=self.header, json=json)
            case "get":
                req = requests.get(url=self.__dmain+self.addr, headers=self.header)
            case "put":
                req = requests.post(url=self.__dmain+self.addr, data=self.data, headers=self.header, json=json)
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
            print(req.status_code)
            return json.loads(req.data)
        else:
            return req
    
    def __call__(self):
        if not (req:=self.status()) and not req.ok:
            print(req)
            return self.failed(status=req.status_code)
        return req

def iscontact(self, contact):
        """check if the contact is valid"""

        phonechecker = re.compile(r'''((\d{3}|\(\d{3}\))? (\s|-|\.)? (\d{3}) (\s|-|\.)? (\d{4}) (\s*(ext|x|ext.)\s*(\d{2,5}))?)''', re.VERBOSE )
        emailchecker = re.compile(r'''(([a-zA-Z0–9_\-\.]) + @ + [a-zA-Z0–9_\-\.] (\.[a-zA-Z]{2,5}))''', re.VERBOSE )
        try:
            if phonechecker.match(contact):
                print(phonechecker.match(contact))
                return True, contact
            elif emailchecker.match(contact):
                print(emailchecker.match(contact))
                return True, contact
            else:
                error = "this is not an email or mobile phone number"
        except KeyboardInterrupt:
            error = "The field can't be empty"
        return error


if __name__ == "__main__":
    def anonym(**data):
        _, d1 = data
        print(d1)
    form = {"fn": "john mba", "cont": "nwanjamba@gmail.com", "pwd": "nalkjiofcji98", "vpwd": "nalkjiofcji98"}
    pg = ReqApi(req_typ="get", req_url="/accounts/api/reg")
    flds = ['Knowledge', 'Class', 'Location', 'Started']
    gdf, fld = form_dict("/app/register", flds)
    print(gdf, fld)

    ok = anonym({"befo": "nower"})
