
import datetime
from itsdangerous import json
from pydantic import BaseModel, validator, Field, PositiveInt, EmailStr
from typing import Optional, Union


class Phone():
    number: str

    @validator('phone')
    def checkName(cls, phone):
        if ' ' not in phone:
            raise ValueError('must contain a space')
        return phone.title()

class LogCheck(BaseModel):
    """check login data"""
    cnt: Union[EmailStr, PositiveInt]
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

class Ip(BaseModel):
    ip: int
    loc: int

class Globe(BaseModel):
    """serialize notification of events from arenas and voice of people of interest"""

    country: str
    region: str
    title: str
    city: str
    postal: str
    locatn: str
    metro: str
    area: str
