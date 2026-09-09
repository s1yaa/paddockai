import uuid
from sqlalchemy import String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from database import Base


class Season(Base):
    __tablename__ = "seasons"

    id:           Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    year:         Mapped[int]       = mapped_column(Integer, unique=True, nullable=False)
    total_rounds: Mapped[int]       = mapped_column(Integer, nullable=False)
    current:      Mapped[bool]      = mapped_column(Boolean, default=False)
    status:       Mapped[str]       = mapped_column(String(32), default="active")

    # Relationships
    races:                Mapped[list["Race"]]                = relationship("Race", back_populates="season")
    driver_standings:     Mapped[list["DriverStanding"]]     = relationship("DriverStanding", back_populates="season")
    constructor_standings: Mapped[list["ConstructorStanding"]] = relationship("ConstructorStanding", back_populates="season")
