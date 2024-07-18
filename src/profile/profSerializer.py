import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field
from pydantic.types import PositiveInt


class Object(BaseModel):
    """check login data"""

    obj: Optional[PositiveInt]


class Place(Object):
    """check login data"""

    arena: Optional[int]
    fld: str
    locatn: str
    strt: datetime.date
    end: Optional[datetime.date]
    dt: datetime.datetime = Field(default=datetime.datetime.now())


class Basics(Place):
    """check login data"""

    acad: bool


class Acads(Place):
    ttl: str
    acad: Optional[bool]


class Resrch(Place):
    """Create a spotlight either from external source or internal source"""

    typ: bool
    emel: EmailStr
    dt: datetime.datetime = Field(default=datetime.datetime.now())
