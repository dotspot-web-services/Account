
from pydantic import BaseModel, IPvAnyAddress


class Ip(BaseModel):
    ipaddr: IPvAnyAddress

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
