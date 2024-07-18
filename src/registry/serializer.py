import datetime
import re
from typing import Union

from pydantic import BaseModel, EmailStr, Field, FilePath, field_validator


class Phone(BaseModel):
    numb: str

    @field_validator("numb")
    @classmethod
    def checkcont(cls, num: field_validator) -> ValueError | str:
        phone = re.compile(
            r"""((\d{3}|\(\d{3}\))? (\s|-|\.)? (\d{3})
                (\s|-|\.)? (\d{4}) (\s*(ext|x|ext.)\s*(\d{2,5}))?
            )""",
            re.VERBOSE,
        )
        if isinstance(num, list):
            for cone in num:
                if phone.match(cone):
                    return cone.title()
        elif phone.match(num):
            return num.title()
        raise ValueError("this is not a phone number")


class Contact(BaseModel):
    """check login data"""

    cont: Union[EmailStr, Phone]


class LogCheck(Contact):
    """check login data"""

    pwd: str


class PwdCheck(LogCheck):
    """Check password"""

    vpwd: str

    @field_validator("vpwd")
    def check_pwd(cls, v: str, values: field_validator) -> ValueError | str:
        if "pwd" in values and v != values["pwd"]:
            raise ValueError("passwords do no match")
        return v


class RegCheck(LogCheck):
    """Check registeration detail"""

    fname: str
    dt: datetime.datetime = Field(default=datetime.datetime.now())

    @field_validator("fname")
    def check_name(cls, name: field_validator) -> ValueError | str:
        if len(name.split(" ")) < 2 > 3:
            raise ValueError("this is not a full name")
        return name.title()


class finalCheck(RegCheck):
    dob: datetime.date
    sx: bool


class Mailer(BaseModel):
    """Serialize email data"""

    subject: str
    content: str
    file: FilePath
