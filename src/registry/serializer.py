
import re
import datetime
from pydantic import BaseModel, FilePath, validator, Field, NameEmail
from typing import Optional, Union


class Phone(BaseModel):
    numb:str

    @validator('numb')
    def checkcont(cls, numb):
        phone = re.compile(r'''((\d{3}|\(\d{3}\))? (\s|-|\.)? (\d{3}) (\s|-|\.)? (\d{4}) (\s*(ext|x|ext.)\s*(\d{2,5}))?)''', re.VERBOSE )
        if isinstance(numb, list):
            for cone in numb:
                if phone.match(cone):
                    return numb.title()
        elif phone.match(numb):
            return numb.title()
        raise ValueError('this is not a phone number')

class Contact(BaseModel):
    """check login data"""
    
    cnt: Union[NameEmail, Phone]

class LogCheck(Contact):
    """check login data"""

    pwd: str

class PwdCheck(LogCheck):
    """Create a spotlight either from external source or internal source"""

    pwd2: str

    @validator('pwd2')
    def check_pwd(cls, v, values):
        if 'pwd' in values and v != values['pwd']:
            raise ValueError('passwords do no match')
        return v

class RegCheck(LogCheck):
    """Create a spotlight either from external source or internal source"""

    fullname: str
    cntyp: bool
    dt = Field(default=datetime.datetime.now())

    @validator('fullname')
    def check_name(cls, fullname):
        if len(fullname.split(' ')) < 2 > 3:
            raise ValueError('this is not a full name')
        return fullname.title()

class finalCheck(RegCheck):
    dob: datetime.date
    pwd: Optional[str]
    pwd2: Optional[str]
    sex: bool

class Mailer(BaseModel):
    """serialize notification of events from arenas and voice of people of interest"""

    subject: str
    content: str
    file: FilePath
