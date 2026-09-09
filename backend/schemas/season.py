import uuid
from pydantic import BaseModel, ConfigDict


class SeasonOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:           uuid.UUID
    year:         int
    total_rounds: int
    current:      bool
    status:       str
