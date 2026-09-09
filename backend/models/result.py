import uuid
from sqlalchemy import String, Integer, Boolean, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from database import Base


class PracticeResult(Base):
    __tablename__ = "practice_results"

    id:              Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id:      Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("sessions.id"), nullable=False)
    driver_id:       Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("drivers.id"), nullable=False)
    constructor_id:  Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("constructors.id"), nullable=False)
    position:        Mapped[int | None]= mapped_column(Integer)
    best_lap_time:   Mapped[str | None]= mapped_column(String(16))
    best_lap_ms:     Mapped[int | None]= mapped_column(Integer)
    gap_to_first_ms: Mapped[int | None]= mapped_column(Integer)
    laps_completed:  Mapped[int | None]= mapped_column(Integer)

    session:     Mapped["Session"]     = relationship("Session", back_populates="practice_results")
    driver:      Mapped["Driver"]      = relationship("Driver")
    constructor: Mapped["Constructor"] = relationship("Constructor")


class QualifyingResult(Base):
    __tablename__ = "qualifying_results"

    id:             Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id:     Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("sessions.id"), nullable=False)
    driver_id:      Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("drivers.id"), nullable=False)
    constructor_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("constructors.id"), nullable=False)
    position:       Mapped[int]       = mapped_column(Integer, nullable=False)
    q1_time:        Mapped[str | None]= mapped_column(String(16))
    q1_ms:          Mapped[int | None]= mapped_column(Integer)
    q2_time:        Mapped[str | None]= mapped_column(String(16))
    q2_ms:          Mapped[int | None]= mapped_column(Integer)
    q3_time:        Mapped[str | None]= mapped_column(String(16))
    q3_ms:          Mapped[int | None]= mapped_column(Integer)
    best_time:      Mapped[str | None]= mapped_column(String(16))
    best_ms:        Mapped[int | None]= mapped_column(Integer)
    gap_to_pole_ms: Mapped[int | None]= mapped_column(Integer)
    eliminated_in:  Mapped[str | None]= mapped_column(String(4))
    penalty:        Mapped[str | None]= mapped_column(String(256))

    session:     Mapped["Session"]     = relationship("Session", back_populates="qualifying_results")
    driver:      Mapped["Driver"]      = relationship("Driver")
    constructor: Mapped["Constructor"] = relationship("Constructor")


class RaceResult(Base):
    __tablename__ = "race_results"

    id:                  Mapped[uuid.UUID]   = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id:          Mapped[uuid.UUID]   = mapped_column(UUID(as_uuid=True), ForeignKey("sessions.id"), nullable=False)
    driver_id:           Mapped[uuid.UUID]   = mapped_column(UUID(as_uuid=True), ForeignKey("drivers.id"), nullable=False)
    constructor_id:      Mapped[uuid.UUID]   = mapped_column(UUID(as_uuid=True), ForeignKey("constructors.id"), nullable=False)
    grid_position:       Mapped[int | None]  = mapped_column(Integer)
    finishing_position:  Mapped[int | None]  = mapped_column(Integer)
    status:              Mapped[str]         = mapped_column(String(64), default="Finished")
    dnf_reason:          Mapped[str | None]  = mapped_column(String(256))
    points:              Mapped[float]       = mapped_column(Numeric(4, 1), default=0)
    fastest_lap:         Mapped[bool]        = mapped_column(Boolean, default=False)
    fastest_lap_time:    Mapped[str | None]  = mapped_column(String(16))
    laps_completed:      Mapped[int | None]  = mapped_column(Integer)
    gap_to_winner:       Mapped[str | None]  = mapped_column(String(32))
    penalty:             Mapped[str | None]  = mapped_column(String(256))

    session:     Mapped["Session"]     = relationship("Session", back_populates="race_results")
    driver:      Mapped["Driver"]      = relationship("Driver")
    constructor: Mapped["Constructor"] = relationship("Constructor")
