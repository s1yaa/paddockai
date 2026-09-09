import uuid
from sqlalchemy import String, Integer, Numeric, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from database import Base


class Circuit(Base):
    __tablename__ = "circuits"

    id:               Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    slug:             Mapped[str]       = mapped_column(String(64), unique=True, nullable=False)
    name:             Mapped[str]       = mapped_column(String(128), nullable=False)
    short_name:       Mapped[str | None]= mapped_column(String(64))
    city:             Mapped[str | None]= mapped_column(String(64))
    country:          Mapped[str]       = mapped_column(String(64), nullable=False)
    country_code:     Mapped[str | None]= mapped_column(String(3))
    latitude:         Mapped[float | None] = mapped_column(Numeric(10, 6))
    longitude:        Mapped[float | None] = mapped_column(Numeric(10, 6))
    length_km:        Mapped[float | None] = mapped_column(Numeric(6, 3))
    corners:          Mapped[int | None]= mapped_column(Integer)
    lap_record:       Mapped[str | None]= mapped_column(String(16))
    lap_record_driver:Mapped[str | None]= mapped_column(String(64))
    lap_record_year:  Mapped[int | None]= mapped_column(Integer)
    circuit_type:     Mapped[str | None]= mapped_column(String(32))  # permanent / street / hybrid
    overtaking_difficulty: Mapped[int | None] = mapped_column(Integer)
    altitude_m:       Mapped[int | None]= mapped_column(Integer)
    time_zone:        Mapped[str | None]= mapped_column(String(64))
    first_gp_year:    Mapped[int | None]= mapped_column(Integer)

    # Relationships
    races: Mapped[list["Race"]] = relationship("Race", back_populates="circuit")
