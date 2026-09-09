import uuid
from datetime import datetime
from sqlalchemy import String, Integer, Boolean, ForeignKey, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from database import Base


class ModelVersion(Base):
    __tablename__ = "model_versions"

    id:                   Mapped[uuid.UUID]       = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name:                 Mapped[str]             = mapped_column(String(64), nullable=False)
    version:              Mapped[str]             = mapped_column(String(32), nullable=False)
    model_type:           Mapped[str]             = mapped_column(String(32), nullable=False)
    training_started_at:  Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    training_finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    dataset_version:      Mapped[str | None]      = mapped_column(String(64))
    training_seasons:     Mapped[str | None]      = mapped_column(String(64))
    validation_season:    Mapped[int | None]      = mapped_column(Integer)
    features:             Mapped[dict | None]     = mapped_column(JSONB)
    metrics:              Mapped[dict | None]     = mapped_column(JSONB)
    active:               Mapped[bool]            = mapped_column(Boolean, default=False)
    notes:                Mapped[str | None]      = mapped_column(Text)
    created_at:           Mapped[datetime]        = mapped_column(DateTime(timezone=True), server_default=func.now())

    prediction_snapshots: Mapped[list["PredictionSnapshot"]] = relationship("PredictionSnapshot", back_populates="model_version")


class PredictionSnapshot(Base):
    __tablename__ = "prediction_snapshots"

    id:               Mapped[uuid.UUID]       = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    race_id:          Mapped[uuid.UUID]       = mapped_column(UUID(as_uuid=True), ForeignKey("races.id"), nullable=False)
    session_id:       Mapped[uuid.UUID | None]= mapped_column(UUID(as_uuid=True), ForeignKey("sessions.id"))
    model_version_id: Mapped[uuid.UUID | None]= mapped_column(UUID(as_uuid=True), ForeignKey("model_versions.id"))
    prediction_type:  Mapped[str]             = mapped_column(String(32), nullable=False)
    stage:            Mapped[str]             = mapped_column(String(64), nullable=False)
    predicted_at:     Mapped[datetime]        = mapped_column(DateTime(timezone=True), server_default=func.now())
    data_version:     Mapped[str | None]      = mapped_column(String(64))
    predictions:      Mapped[dict]            = mapped_column(JSONB, nullable=False)
    probabilities:    Mapped[dict | None]     = mapped_column(JSONB)
    expected_points:  Mapped[dict | None]     = mapped_column(JSONB)
    metadata_json:    Mapped[dict | None]     = mapped_column("metadata", JSONB)
    created_at:       Mapped[datetime]        = mapped_column(DateTime(timezone=True), server_default=func.now())

    race:          Mapped["Race"]          = relationship("Race", back_populates="prediction_snapshots")
    model_version: Mapped["ModelVersion"]  = relationship("ModelVersion", back_populates="prediction_snapshots")


class SimulationRun(Base):
    __tablename__ = "simulation_runs"

    id:               Mapped[uuid.UUID]       = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    season_id:        Mapped[uuid.UUID]       = mapped_column(UUID(as_uuid=True), ForeignKey("seasons.id"), nullable=False)
    model_version_id: Mapped[uuid.UUID | None]= mapped_column(UUID(as_uuid=True), ForeignKey("model_versions.id"))
    from_race_id:     Mapped[uuid.UUID | None]= mapped_column(UUID(as_uuid=True), ForeignKey("races.id"))
    n_simulations:    Mapped[int]             = mapped_column(Integer, nullable=False)
    scenario_type:    Mapped[str]             = mapped_column(String(32), default="baseline")
    scenario_params:  Mapped[dict | None]     = mapped_column(JSONB)
    results:          Mapped[dict]            = mapped_column(JSONB, nullable=False)
    ran_at:           Mapped[datetime]        = mapped_column(DateTime(timezone=True), server_default=func.now())


class FeatureSnapshot(Base):
    __tablename__ = "feature_snapshots"

    id:            Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    race_id:       Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("races.id"), nullable=False)
    driver_id:     Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("drivers.id"), nullable=False)
    snapshot_type: Mapped[str]       = mapped_column(String(32), default="pre_race")
    features:      Mapped[dict]      = mapped_column(JSONB, nullable=False)
    created_at:    Mapped[datetime]  = mapped_column(DateTime(timezone=True), server_default=func.now())
