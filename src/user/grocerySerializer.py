
import datetime

from pydantic import BaseModel, FilePath, Field, PositiveInt
from typing import Optional


class Object(BaseModel):

    obj: Optional[PositiveInt]

class CreateAward(Object):
    """Create a spotlight either from external source or internal source"""

    plc: str
    acts: bool
    title: int
    awdt: datetime.date
    dt = Field(default=datetime.datetime.now())

class CreatePub(Object):
    """Create a spotlight either from external source or internal source"""

    instn: PositiveInt
    dfld: str
    dttl: str
    med: FilePath
    pdt: datetime.date
    dt = Field(default=datetime.datetime.now())

class CreateSoc(Object):
    """serialize notification of events from arenas and voice of people of interest"""

    title: str
    typ: str
    timestamp = Field(default=datetime.datetime.now())


