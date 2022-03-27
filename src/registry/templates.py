
import os
from curses.ascii import isalnum
import imghdr
from dns.resolver import query

from setting.decs import Auth as __auth


FILE_PATH = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(FILE_PATH)
TEMP_DIR = os.path.join(BASE_DIR, "templates")



class Template:

    temp_name = ""
    context = None
        
    def __init__(self, temp_name="", context=None, *args, **kwargs) -> None:
        self.temp_name = temp_name
        self.context = context

    def get_temp(self):
        temp_path = os.path.join(TEMP_DIR, self.temp_name)
        if not os.path.exists(temp_path):
            raise Exception("this path does not exist")
        temp_string = ""
        with open(temp_path, "r") as f:
            temp_string = f.read()
        return temp_string

    def render(self, context=None):
        render_ctxt = context
        if self.context is not None:
            render_ctxt = self.context
        if not isinstance(render_ctxt, dict):
            render_ctxt = {}
        temp_string = self.get_temp()
        return temp_string.format(**render_ctxt)


class SetMail:

    contact = None
    isemail = True
    phone = set()
    domain = set()
    confirm_acc = False
    has_html = False
    toname=None
    subject=None
    text=None
    link_text = None
    attatchment=None
    req_device = None

    def __init__(self, contact, subject=None, toname=None, text=None, attatchment=None):

        assert contact is not None
        if not isinstance(contact, str):
            self.contact = set(contact)
        else:
            self.contact = contact
        if subject == "reset" and text is not None:
            self.subject = "Password reset"
            self.link_text = "Reset password"
        elif subject == "confirm" and text is not None:
            self.subject = "Confirmation your email"
            self.link_text = "Confirm email"
            self.confirm_acc = True
        else:
            assert subject and text is not None
            self.subjt = subject
        self.name = toname
        if self.text is not None:
            self.text = text
        self.attatchd = attatchment

    def link(self):
        __token = __auth(func=self.toname["id"])
        link = f"<a href='questarenz.com?token={__token.encode_auth(day=1)}' >{self.link_text}</a>"
        return link

    def verifymail(self, dormain):
        
        records = query(dormain, 'MX')
        mxRecord = records[0].exchange
        if mxRecord:
            return
    
    def domain(self):

        if isinstance(self.contact, str):
            if not self.verifymail(dormain=str(self.contact.split('@')[1])):
                return "invaliid dormain"
            return
        elif isinstance(self.contact, (list, tuple, set)):
            self.isemail = False
            return
        else:
            for item in self.contact:
                (splitAddress := item.split('@'))
                if self.verifymail(dormain=str(splitAddress[1])):
                    self.domain.add(item)
                elif isalnum(item):
                    self.phone.add(item)
        return

    def file(self, file):
        with open(file, "rb") as f:
            f_data = f.read()
            f_typ = imghdr.what(f.name)
            f_name = f.name
        if f_name in self._db._oda.allowed_extension:
            return f_data, f_typ, f_name
        return f_data, f_name

    def define_msg(self, device):

        if self.confirm_acc:
            content = f"""
            Hi... {self.toname["usr"]} you are welcome to Questarenz, Please confirm your email to continue in your conquest.
            click to {self.link()}
            """
        elif not self.confirm_acc:
            content = f"""
            have requested for change of password using {device} If you are not the one ignore this email"
            click to {self.link()}
            """
        else:
            content = self.text
        msg = Template(temp_name="gen", context=content)
        return msg
