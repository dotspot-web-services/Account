
from datetime import datetime
from pydantic import BaseModel, validator, FilePath, Field, PositiveInt, EmailStr
from typing import Union, Optional

from setting.dbcon import DbSet as db


class Usr(BaseModel):
    """Create a spotlight either from external source or internal source"""

    id: PositiveInt
    name: str
    avatar: FilePath

    @validator('name')
    def checkName(cls, name):
        if ' ' not in name:
            raise ValueError('must contain a space')
        return name.title()

class Phone(BaseModel):
    number: str

    @validator('phone')
    def checkName(cls, phone):
        if ' ' not in phone:
            raise ValueError('must contain a space')
        return phone.title()

class LogCheck(BaseModel):
    """check login data"""
    cnt: Union[EmailStr, Phone]
    pwd: str

class RegCheck(LogCheck):
    """Create a spotlight either from external source or internal source"""

    fullname: str
    dob: datetime.date
    pwd: str
    pwd2: str
    cntyp: bool
    sex: bool
    ip: str
    dt = Field(default=datetime.now())

    @validator('pwd2')
    def check_pwd(cls, v, values):
        if 'pwd' in values and v != values['pwd1']:
            raise ValueError('passwords do no match')
        return v

    @validator('fullname')
    def check_pwd(cls, fullname):
        if len(fullname.split(' ') < 2 > 3):
            raise ValueError('this is not a full name')
        return fullname.title()

class SerializedLimelight(Usr):
    """serialize notification of events from arenas and voice of people of interest"""

    objid: PositiveInt
    src: Usr
    title: str
    files: Union[FilePath, list]
    descn: Optional[str]
    timestamp = Field(default=datetime.now())

    def __init__(__pydantic_self__, **data: int) -> None:
        soc_count = db._model.soc_count(db.get_db, data.get('objid'))
        if soc_count:
            data["ctn"] = soc_count.get('ctns')
            data["vce"] = soc_count.get('vces')
            data['rxn'] = soc_count.get('rxns')
        super().__init__(**data)
    class Config:
        extra = 'forbid'
