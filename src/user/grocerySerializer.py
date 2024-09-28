import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt


class Object(BaseModel):
    obj: Optional[PositiveInt]


class CreateAward(Object):
    """Check award data"""

    plc: str
    acts: str
    ttl: int
    awdt: datetime.date
    dt: datetime.datetime = Field(default=datetime.datetime.now())


class CreateSoc(Object):
    """
    serialize notification of events from arenas
    voice of people of interest
    """

    title: str
    typ: str
    timestamp: datetime.datetime = Field(default=datetime.datetime.now())
