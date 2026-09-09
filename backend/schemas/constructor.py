import uuid
from pydantic import BaseModel, ConfigDict


class ConstructorListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:              uuid.UUID
    slug:            str
    name:            str
    short_name:      str | None
    nationality:     str | None
    color_primary:   str | None
    color_secondary: str | None
    engine_supplier: str | None
    championships:   int


class ConstructorOut(ConstructorListItem):
    base:        str | None
    principal:   str | None
    first_season: int | None
