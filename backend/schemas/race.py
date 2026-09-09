import uuid
from datetime import date, datetime
from pydantic import BaseModel, ConfigDict
from .circuit import CircuitOut


class SessionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:           uuid.UUID
    session_type: str
    scheduled_at: datetime | None
    status:       str


class RaceListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:           uuid.UUID
    round_number: int
    gp_name:      str
    country:      str | None
    date:         date | None
    status:       str
    has_sprint:   bool
    circuit:      CircuitOut | None


class RaceOut(RaceListItem):
    official_name: str | None
    season_id:     uuid.UUID


class RaceDetail(RaceOut):
    sessions: list[SessionOut] = []


