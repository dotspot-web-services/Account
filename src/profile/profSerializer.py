
import datetime
from pydantic import BaseModel, validator, FilePath, Field, PositiveInt, EmailStr
from typing import Union, Optional

from setting.dbcon import DbSet as db


class Usr(BaseModel):
    """Create a spotlight either from external source or internal source"""

    fullname: Optional[str]
    avatar: Optional[FilePath]

    @validator('fullname')
    def check_name(cls, fullname):
        if ' ' not in fullname:
            raise ValueError('must contain a space')
        return fullname.title()

class SerializedBasics(Usr):
    """serialize user registeration data for update"""

    cnt: bool
    dob: datetime.date
    sex: bool

class Basics(BaseModel):
    """check login data"""

    arena: Optional[int]
    dspln: str
    place: str
    strtd: datetime.date
    endd: datetime.date
    acad: bool

class Acads(Basics):
    base: int
    ttl: str
    acad: Optional[bool]

class Resrch(BaseModel):
    """Create a spotlight either from external source or internal source"""

    acad: int
    typ: bool
    org: str
    displn: str
    email = EmailStr
    strtd: datetime.date
    endd: datetime.date
    dt = Field(default=datetime.datetime.now())

class Workplace(BaseModel):
    """Create a spotlight either from external source or internal source"""

    arena: str
    plc: str
    rol: bool
    strtd: datetime.date
    endd: datetime.date
    dt = Field(default=datetime.datetime.now())

class SerializedProf(Usr):
    """serialize notification of events from arenas and voice of people of interest"""

    objid: PositiveInt
    src: Usr
    title: str
    files: Union[FilePath, list]
    descn: Optional[str]
    timestamp = Field(default=datetime.datetime.now())

    def __init__(__pydantic_self__, **data: int) -> None:
        soc_count = db._model.soc_count(db.get_db, data.get('objid'))
        if soc_count:
            data["ctn"] = soc_count.get('ctns')
            data["vce"] = soc_count.get('vces')
            data['rxn'] = soc_count.get('rxns')
        super().__init__(**data)
    class Config:
        extra = 'forbid'
        arbitrary_types_allowed = True
