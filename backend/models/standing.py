import uuid
from sqlalchemy import Integer, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from database import Base


class DriverStanding(Base):
    __tablename__ = "driver_standings"

    id:            Mapped[uuid.UUID]   = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    season_id:     Mapped[uuid.UUID]   = mapped_column(UUID(as_uuid=True), ForeignKey("seasons.id"), nullable=False)
    driver_id:     Mapped[uuid.UUID]   = mapped_column(UUID(as_uuid=True), ForeignKey("drivers.id"), nullable=False)
    constructor_id:Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("constructors.id"))
    position:      Mapped[int | None]  = mapped_column(Integer)
    points:        Mapped[float]       = mapped_column(Numeric(6, 1), default=0)
    wins:          Mapped[int]         = mapped_column(Integer, default=0)
    podiums:       Mapped[int]         = mapped_column(Integer, default=0)
    poles:         Mapped[int]         = mapped_column(Integer, default=0)
    dnfs:          Mapped[int]         = mapped_column(Integer, default=0)
    races_entered: Mapped[int]         = mapped_column(Integer, default=0)
    updated_at:    Mapped[DateTime]    = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    season:      Mapped["Season"]      = relationship("Season", back_populates="driver_standings")
    driver:      Mapped["Driver"]      = relationship("Driver", back_populates="standings")
    constructor: Mapped["Constructor"] = relationship("Constructor", back_populates="driver_standings")


class ConstructorStanding(Base):
    __tablename__ = "constructor_standings"

    id:             Mapped[uuid.UUID]  = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    season_id:      Mapped[uuid.UUID]  = mapped_column(UUID(as_uuid=True), ForeignKey("seasons.id"), nullable=False)
    constructor_id: Mapped[uuid.UUID]  = mapped_column(UUID(as_uuid=True), ForeignKey("constructors.id"), nullable=False)
    position:       Mapped[int | None] = mapped_column(Integer)
    points:         Mapped[float]      = mapped_column(Numeric(6, 1), default=0)
    wins:           Mapped[int]        = mapped_column(Integer, default=0)
    podiums:        Mapped[int]        = mapped_column(Integer, default=0)
    updated_at:     Mapped[DateTime]   = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    season:      Mapped["Season"]      = relationship("Season", back_populates="constructor_standings")
    constructor: Mapped["Constructor"] = relationship("Constructor", back_populates="constructor_standings")
