import uuid
from pydantic import BaseModel, ConfigDict


class CircuitOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:                   uuid.UUID
    slug:                 str
    name:                 str
    short_name:           str | None
    city:                 str | None
    country:              str
    country_code:         str | None
    length_km:            float | None
    corners:              int | None
    circuit_type:         str | None
    overtaking_difficulty:int | None
    lap_record:           str | None
    lap_record_driver:    str | None
    lap_record_year:      int | None
    first_gp_year:        int | None
    latitude:             float | None
    longitude:            float | None
