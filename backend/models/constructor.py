import uuid
from sqlalchemy import String, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from database import Base


class Constructor(Base):
    __tablename__ = "constructors"

    id:              Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    slug:            Mapped[str]       = mapped_column(String(64), unique=True, nullable=False)
    name:            Mapped[str]       = mapped_column(String(128), nullable=False)
    short_name:      Mapped[str | None]= mapped_column(String(32))
    nationality:     Mapped[str | None]= mapped_column(String(64))
    base:            Mapped[str | None]= mapped_column(String(128))
    principal:       Mapped[str | None]= mapped_column(String(128))
    color_primary:   Mapped[str | None]= mapped_column(String(7))
    color_secondary: Mapped[str | None]= mapped_column(String(7))
    engine_supplier: Mapped[str | None]= mapped_column(String(64))
    first_season:    Mapped[int | None]= mapped_column(Integer)
    championships:   Mapped[int]       = mapped_column(Integer, default=0)

    # Relationships
    drivers:          Mapped[list["Driver"]]      = relationship("Driver", back_populates="constructor")
    driver_standings: Mapped[list["DriverStanding"]]      = relationship("DriverStanding", back_populates="constructor")
    constructor_standings: Mapped[list["ConstructorStanding"]] = relationship("ConstructorStanding", back_populates="constructor")
