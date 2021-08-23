
import datetime

from pydantic import BaseModel, validator, FilePath, Field, PositiveInt
from typing import Optional

from setting.dbcon import DbSet as db


class Usr(BaseModel):
    """Create a spotlight either from external source or internal source"""

    name: str
    avatar: FilePath

    @validator('name')
    def name_must_contain_space(cls, name):
        if ' ' not in name:
            raise ValueError('must contain a space')
        return name.title()

class CreateAward(BaseModel):
    """Create a spotlight either from external source or internal source"""

    typ: bool
    arena: int
    org: str
    med: FilePath
    awdt: datetime.date
    dt = Field(default=datetime.datetime.now())

class Createpub(BaseModel):
    """Create a spotlight either from external source or internal source"""

    rsrch: PositiveInt
    dfld: str
    dttl: str
    med: FilePath
    pdt: datetime.date
    dt = Field(default=datetime.datetime.now())

class CreateStory(BaseModel):
    """serialize search results"""

    title: str
    sumry: str
    dt = Field(default=datetime.datetime.now())

class CreateStoryvasn(BaseModel):
    """serialize search results"""

    stry: PositiveInt
    adding: bool
    title: str
    vason: str
    refdt: datetime.date
    dt = Field(default=datetime.datetime.now())

class CreateQuote(BaseModel):
    """serialize list of events that requires user attention including its source"""

    vasn: PositiveInt
    qot: str
    dt = Field(default=datetime.datetime.now())

class SerializedLimelight(Usr):
    """serialize notification of events from arenas and voice of people of interest"""

    objid: PositiveInt
    src: Usr
    title: str
    files: FilePath
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
