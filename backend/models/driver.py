import uuid
from datetime import date
from sqlalchemy import String, Integer, Boolean, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from database import Base


class Driver(Base):
    __tablename__ = "drivers"

    id:             Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    slug:           Mapped[str]       = mapped_column(String(64), unique=True, nullable=False)
    first_name:     Mapped[str]       = mapped_column(String(64), nullable=False)
    last_name:      Mapped[str]       = mapped_column(String(64), nullable=False)
    abbreviation:   Mapped[str | None]= mapped_column(String(3))
    number:         Mapped[int | None]= mapped_column(Integer)
    nationality:    Mapped[str | None]= mapped_column(String(64))
    country_code:   Mapped[str | None]= mapped_column(String(3))
    date_of_birth:  Mapped[date | None] = mapped_column(Date)
    constructor_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("constructors.id"))
    active:         Mapped[bool]      = mapped_column(Boolean, default=True)
    championships:  Mapped[int]       = mapped_column(Integer, default=0)
    career_wins:    Mapped[int]       = mapped_column(Integer, default=0)
    career_podiums: Mapped[int]       = mapped_column(Integer, default=0)
    career_poles:   Mapped[int]       = mapped_column(Integer, default=0)

    # Relationships
    constructor: Mapped["Constructor"] = relationship("Constructor", back_populates="drivers")
    standings:   Mapped[list["DriverStanding"]] = relationship("DriverStanding", back_populates="driver")
