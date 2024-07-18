import os
import shutil
import smtplib
from typing import Any

import requests
from dns.resolver import query
from flask import flash, redirect, render_template, request, session, url_for
from pydantic import FilePath, ValidationError


def verifymail(dormain: str, host: str, mail: str) -> bool | None:
    server = smtplib.SMTP()
    records = query(dormain, "MX")
    mxRecord = records[0].exchange
    if mxRecord:
        mxRecord = str(mxRecord)
        # SMTP lib setup (use debug level for full output)
        server.set_debuglevel(0)
        # SMTP Conversation
        server.connect(mxRecord)
        # server.local_hostname(Getlocal server hostname)
        server.helo(server.local_hostname)
        server.mail(host)
        code, message = server.rcpt(str(mail))
        server.quit()
        if code == 250:  # Assume SMTP response 250 is success
            print("Success")
            return True
    print("Bad")
    print(code)
    print(message)
    return False


def downloader(url: str, directory: str, fname: FilePath | str = "") -> FilePath:
    """_summary_

    Args:
        url (_type_):  _description_
        directory (_type_):  _description_
        fname (_type_, optional):  _description_. Defaults to None.
    """
    if fname == "":
        fname = os.path.basename(url)
    dl_path = os.path.join(directory, fname)
    with requests.get(url, stream=True) as r:
        with open(dl_path, "wb") as f:
            shutil.copyfileobj(fsrc=r.raw, fdst=f)
    return dl_path


def handle_ui_response(
    status: int, data: dict[str, str], flas: str = ""
) -> render_template | redirect | None:
    """_summary_

    Args:
        status (_type_):  _description_
        data (_type_):  _description_
        flas (str, optional):  _description_. Defaults to "".
    """

    if status == 200:
        session["active"] = False
        session["token"] = data
        page = redirect(url_for("accs.regs.finalize"))
    elif status == 422:
        return render_template(
            "/registry/reg.html",
            endpt=url_for("accs.regs.regPage"),
            fields="register",
            data=data,
        )
    else:
        if status == 409:
            flash(message="Account already exists, please login", category="info")
            page = redirect(request.url)
    return page


def convert_errors(err: ValidationError) -> dict[str, str]:
    """_summary_

    Args:
        err (_type_):  _description_

    Raises:
        Exception:  _description_

    Returns:
        _type_:  _description_
    """

    error: dict[str, str] = {}
    for item in err.errors():
        error[item.get("loc")[0]] = item.get("msg")
    return error


class FormData:
    """This class is used with jinja to generate template"""

    def __init__(
        self,
        endpt: str,
        form_fields: str,
        **extras: Any,
    ) -> None:
        """Generate dictionary of inputs for instructing jinja templating

        Args:
            endpt (str): url endpoint to process form
            fields (dict, optional): name and label of form input. Defaults={}.
            registry (str, optional): login, register, contact,
            email or number. Defaults to ''.
        """
        form_fields = form_fields
        self.extras = extras
        self.endpt: str = endpt
        default_form: list[str] = [
            "contact",
            "recover",
            "register",
            "login",
            "work",
            "research",
            "accademic",
            "basic",
            "award",
            "social",
        ]

        if isinstance(form_fields, str):
            self._registry = True
            form_fields = form_fields.lower()
        if form_fields not in default_form and not isinstance(form_fields, dict):
            raise Exception(
                "fieldsError:  Fields is either default form or input fields"
            )
        if form_fields in default_form[0:4]:
            self.fields, self.extras = self.regData(value=form_fields)
        if form_fields in default_form[5:-3]:
            self.fields, self.extras = self.profData(value=form_fields)
        if form_fields in default_form[-2:-1]:
            self.fields, self.extras = self.usrData(value=form_fields)
        self.prof: dict[str, str] = {
            "emel": "Email",
            "displn": "Discipline",
            "plc": "Institution",
            "org": "Organisation",
            "cls": "Class",
            "locatn": "Location",
            "rol": "Role",
            "knwlg": "Knowledge",
            "fld": "Field",
            "resech": "Type of Research",
            "ttl": "Title",
            "strt": "Start",
            "end": "End",
        }

    def form(self) -> dict[str, dict[str, str]] | dict[str, str]:
        form_attr: dict[str, dict[str, str]] | dict[str, str] = {
            "action": f"{self.endpt}"
        }
        form_attr["method"] = self.extras.get("method", "POST")
        form_attr["button"] = self.extras.get("button", {"label": "Create"})
        return form_attr

    def regData(self, value: str) -> tuple[dict[str, str], dict[str, dict[str, str]]]:
        """Generate registeration data"""
        regInp: dict[str, str] = {
            "fname": "Full Name",
            "cont": "Contact",
            "pwd": "password",
            "pwd2": "Confirm password",
            "tnc": "I accept the {}, {} and {} of this site.",
        }
        fields: dict[str, str] = {}
        extras: Any = {}

        if value.lower() == "login":
            fields = {"cont": regInp["cont"], "pwd": regInp["pwd"]}
            extras = {
                "pwd": {
                    "note": {"a": {"Reset password": "/accounts/app/contact"}},
                    "type": "password",
                },
                "button": {"label": "Login"},
            }
        elif value.lower() == "register":
            fields = regInp
            extras = {
                "tnc": {
                    "type": "checkbox",
                    "label": {
                        "a": (
                            {"Terms": "tnc.html"},
                            {"Conditions": "tnc.html"},
                            {"privacy policy": "tnc.html"},
                        )
                    },
                },
                "pwd": {"type": "password"},
                "pwd2": {"type": "password"},
                "fn": {"placeholder": "Seperate names with space"},
            }
        elif value.lower() == "recover":
            fields = {"pwd": regInp["pwd"], "pwd2": regInp["pwd2"]}
            extras = {
                "button": {"label": "Reset"},
                "pwd": {"type": "password"},
                "pwd2": {"placeholder": "Confirm password", "type": "password"},
            }
        elif value.lower() == "contact":
            fields = {"cont": regInp["cont"]}
            extras = {
                "cont": {"placeholder": "Enter email or phone number"},
                "button": {"label": "Submit"},
            }
        elif value.lower() == "email":
            fields = {"emel": "Email"}
        return fields, extras

    def profData(self, value: str) -> tuple[dict[str, str], dict[str, dict[str, str]]]:
        plc: dict[str, str] = {
            "locatn": "Institution",
            "fld": "Field",
            "edu": "Knowledge",
        }
        duratn: dict[str, str] = {"strt": "Start", "end": "End"}
        fields: dict[str, str] = {}
        extras: dict[str, dict[str, str]] = {}

        if value.lower() == "basic":
            plc["locatn"] = "Location"
            plc.update(duratn)
            fields = plc
            extras = {"fld": {"placeholder": "E.g an accademy, sciences, arts"}}
        elif value.lower() == "accademic":
            plc["spec"] = "Specialization"
            plc["ttl"] = "Title"
            plc.update(duratn)
            fields = plc
            extras = {"ttl": {"type": "search"}}
        elif value.lower() == "research":
            plc["emel"] = "Email"
            plc["typ"] = "Type of Research"
            plc.update(duratn)
            fields = plc
            extras = {
                "emel": {
                    "placeholder": "organisation or institution email",
                    "type": "email",
                }
            }
        elif value.lower() == "work":
            fields = {"org": "Organisation", "rol": "Role"}
            plc.update(duratn)
            fields = plc
            extras = {"rol": {"placeholder": "The job rol or position"}}
        return fields, extras

    def usrData(self, value: str) -> tuple[dict[str, str], dict[str, dict[str, str]]]:
        if value.lower() == "award":
            fields = {"titl": "Organisation", "typ": "Role"}
            extras = {"rol": {"placeholder": "The job rol or position"}}
        elif value.lower() == "social":
            fields = {
                "plc": "Organisation",
                "acts": "Role",
                "ttl": "Title",
                "awdt": "Date",
            }
            extras = {"rol": {"placeholder": "The job rol or position"}}
        return fields, extras

    def geninp(self, name: str) -> dict[str, str]:
        """Check if theres an extra configs for an input with the name and
        Generate and return an input for the form

        Args:
            name (str): Name of an input with extras used as key in extras
            typ (string): _description_
            label (strin): _description_
        """

        inpt: dict[str, str] = {}
        extattr: dict[str, str] = self.extras.get(name, {})

        if extattr:
            inpt.update(extattr)
        if self._registry and name != "end":
            inpt["required"] = "required"
        inpt["name"] = name
        return inpt

    def form_dict(
        self,
    ) -> tuple[dict[str, dict[str, str]] | dict[str, str], dict[str, dict[str, str]]]:
        """[summary]

        Args:
            endpt ([type]): [description]

        Returns:
            [type]: [description]
        """

        inputs: dict[str, dict[str, str]] = {
            val: self.geninp(name=key) for key, val in self.fields.items()
        }
        return self.form(), inputs

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.form_dict()


if __name__ == "__main__":
    def_form = FormData(endpt="url_for('accs.regs.regPage')", form_fields="contact")()
    print(def_form)
