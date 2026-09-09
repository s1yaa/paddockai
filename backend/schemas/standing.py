import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class DriverStandingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:             uuid.UUID
    position:       int | None
    points:         float
    wins:           int
    podiums:        int
    poles:          int
    dnfs:           int
    races_entered:  int
    driver_id:      uuid.UUID
    constructor_id: uuid.UUID | None
    # Populated via join
    driver_slug:    str | None = None
    driver_name:    str | None = None
    driver_abbr:    str | None = None
    driver_number:  int | None = None
    driver_nationality: str | None = None
    constructor_name: str | None = None
    constructor_slug: str | None = None
    constructor_color: str | None = None
    updated_at:     datetime | None = None


class ConstructorStandingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:               uuid.UUID
    position:         int | None
    points:           float
    wins:             int
    podiums:          int
    constructor_id:   uuid.UUID
    constructor_name: str | None = None
    constructor_slug: str | None = None
    constructor_color: str | None = None
    updated_at:       datetime | None = None
