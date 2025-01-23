from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String
from typing import List

from process_navigator.extensions.database import Base


class Input(Base):
    __tablename__ = "input"
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    CAS: Mapped[str] = mapped_column(nullable=False, unique=True)
    unit_id: Mapped[int] = mapped_column(ForeignKey("unit.id"), nullable=False)

    unit: Mapped["Unit"] = relationship("Unit", back_populates="inputs")
    input_values: Mapped[List["InputValue"]] = relationship(
        "InputValue", back_populates="input"
    )

    def __repr__(self):
        return "Parameter {name} ({symbol})".format(
            name=self.name, symbol=self.unit.symbol
        )
