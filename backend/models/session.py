import uuid
from datetime import datetime
from sqlalchemy import String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from database import Base


class Session(Base):
    __tablename__ = "sessions"

    id:               Mapped[uuid.UUID]       = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    race_id:          Mapped[uuid.UUID]       = mapped_column(UUID(as_uuid=True), ForeignKey("races.id"), nullable=False)
    session_type:     Mapped[str]             = mapped_column(String(32), nullable=False)
    scheduled_at:     Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    status:           Mapped[str]             = mapped_column(String(32), default="upcoming")
    openf1_session_key: Mapped[int | None]   = mapped_column(Integer)

    # Relationships
    race:               Mapped["Race"]                       = relationship("Race", back_populates="sessions")
    practice_results:   Mapped[list["PracticeResult"]]       = relationship("PracticeResult", back_populates="session")
    qualifying_results: Mapped[list["QualifyingResult"]]     = relationship("QualifyingResult", back_populates="session")
    race_results:       Mapped[list["RaceResult"]]           = relationship("RaceResult", back_populates="session")
