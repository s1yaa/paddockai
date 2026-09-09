import uuid
from datetime import date
from sqlalchemy import String, Integer, Boolean, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from database import Base


class Race(Base):
    __tablename__ = "races"

    id:              Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    season_id:       Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("seasons.id"), nullable=False)
    circuit_id:      Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("circuits.id"))
    round_number:    Mapped[int]       = mapped_column(Integer, nullable=False)
    gp_name:         Mapped[str]       = mapped_column(String(128), nullable=False)
    official_name:   Mapped[str | None]= mapped_column(String(256))
    country:         Mapped[str | None]= mapped_column(String(64))
    date:            Mapped[date | None] = mapped_column(Date)
    status:          Mapped[str]       = mapped_column(String(32), default="upcoming")
    has_sprint:      Mapped[bool]      = mapped_column(Boolean, default=False)
    openf1_meeting_key: Mapped[int | None] = mapped_column(Integer)

    # Relationships
    season:   Mapped["Season"]       = relationship("Season", back_populates="races")
    circuit:  Mapped["Circuit"]      = relationship("Circuit", back_populates="races")
    sessions: Mapped[list["Session"]]= relationship("Session", back_populates="race", cascade="all, delete-orphan")
    prediction_snapshots: Mapped[list["PredictionSnapshot"]] = relationship("PredictionSnapshot", back_populates="race")
