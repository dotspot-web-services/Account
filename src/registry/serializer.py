
import re
import datetime
from pydantic import BaseModel, FilePath, validator, Field, EmailStr
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
    
    cont: Union[EmailStr, Phone]

class LogCheck(Contact):
    """check login data"""

    pwd: str

class PwdCheck(LogCheck):
    """Create a spotlight either from external source or internal source"""

    vpwd: str

    @validator('vpwd')
    def check_pwd(cls, v, values):
        if 'pwd' in values and v != values['pwd']:
            raise ValueError('passwords do no match')
        return v

class RegCheck(LogCheck):
    """Create a spotlight either from external source or internal source"""

    fname: str
    dt = Field(default=datetime.datetime.now())

    @validator('fname')
    def check_name(cls, fname):
        if len(fname.split(' ')) < 2 > 3:
            raise ValueError('this is not a full name')
        return fname.title()

class finalCheck(RegCheck):
    dob: datetime.date
    pwd: Optional[str]
    vpwd: Optional[str]
    sx: bool

class Mailer(BaseModel):
    """serialize notification of events from arenas and voice of people of interest"""

    subject: str
    content: str
    file: FilePath
