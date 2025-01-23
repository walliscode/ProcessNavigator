from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from process_navigator.extensions.database import Base


class Param(Base):
    __tablename__ = "param"
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    unit_id: Mapped[int] = mapped_column(ForeignKey("unit.id"), nullable=False)

    unit: Mapped["Unit"] = relationship("Unit", back_populates="parameters")

    param_values: Mapped[List["ParamValue"]] = relationship(
        "ParamValue", back_populates="param"
    )

    def __repr__(self):
        return "Parameter {name} ({symbol})".format(
            name=self.name, symbol=self.unit.symbol
        )
