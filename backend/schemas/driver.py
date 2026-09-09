import uuid
from datetime import date
from pydantic import BaseModel, ConfigDict


class ConstructorRef(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:           uuid.UUID
    slug:         str
    name:         str
    short_name:   str | None
    color_primary: str | None


class DriverListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:           uuid.UUID
    slug:         str
    first_name:   str
    last_name:    str
    abbreviation: str | None
    number:       int | None
    nationality:  str | None
    country_code: str | None
    active:       bool
    constructor:  ConstructorRef | None


class DriverOut(DriverListItem):
    championships:  int
    career_wins:    int
    career_podiums: int
    career_poles:   int
    date_of_birth:  date | None
