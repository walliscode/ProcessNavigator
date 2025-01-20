from typing import List

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from process_navigator.extensions.database import Base, db


class BaseUnit(Base):
    __tablename__ = "base_unit"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    name: Mapped[str] = mapped_column(nullable=False)
    symbol: Mapped[str] = mapped_column(nullable=False)

    unit_combinations: Mapped[List["UnitCombination"]] = relationship(
        "UnitCombination", back_populates="base_unit", init=False
    )

    def __repr__(self):
        return f"<Base Unit {self.name}>"


class UnitModifier(Base):
    __tablename__ = "unit_modifier"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    name: Mapped[str] = mapped_column(nullable=False)
    symbol: Mapped[str] = mapped_column(nullable=False)
    multiplier: Mapped[float] = mapped_column(nullable=False)

    unit_combinations: Mapped[List["UnitCombination"]] = relationship(
        "UnitCombination", back_populates="unit_modifier", init=False
    )

    def __repr__(self):
        return f"<Unit Modifier {self.name}>"


class Unit(Base):
    __tablename__ = "unit"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    name: Mapped[str] = mapped_column(nullable=False)

    unit_combinations: Mapped[List["UnitCombination"]] = relationship(
        "UnitCombination", back_populates="unit", init=False
    )

    parameters: Mapped[List["Param"]] = relationship(
        "Param", back_populates="unit", init=False
    )

    @hybrid_property
    def symbol(self):
        symbol = ""

        if self.unit_combinations is not None:
            for unit_combination in self.unit_combinations:
                base_unit = unit_combination.base_unit
                unit_modifier = unit_combination.unit_modifier

                if unit_modifier:
                    symbol += unit_modifier.symbol

                symbol += base_unit.symbol

                if unit_combination.exponent != 1:
                    symbol += "^"
                    symbol += str(unit_combination.exponent)

        return symbol

    def __repr__(self):
        return "Unit {name} ({symbol})".format(name=self.name, symbol=self.symbol)


class UnitCombination(Base):
    __tablename__ = "unit_combination"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    unit_id: Mapped[int] = mapped_column(db.ForeignKey("unit.id"), nullable=False)
    base_unit_id: Mapped[int] = mapped_column(
        db.ForeignKey("base_unit.id"), nullable=False
    )
    unit_modifier_id: Mapped[int] = mapped_column(
        db.ForeignKey("unit_modifier.id"), nullable=True
    )
    exponent: Mapped[int] = mapped_column(nullable=False)

    unit: Mapped["Unit"] = relationship("Unit", back_populates="unit_combinations")
    base_unit: Mapped["BaseUnit"] = relationship(
        "BaseUnit", back_populates="unit_combinations"
    )
    unit_modifier: Mapped["UnitModifier"] = relationship(
        "UnitModifier", back_populates="unit_combinations"
    )

    def __repr__(self):
        return f"<Unit Combination {self.unit}>"
