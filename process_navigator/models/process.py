"""Contains sqlalchemy models for the process_navigator app."""

from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String

from process_navigator.extensions.database import Base, db


# Define the models for the database
# an Entity represents a physical object that can be isolated and analysed. This is up to some interpretation by the user
class Entity(Base):
    __tablename__ = "entity"
    id: Mapped[int] = mapped_column(primary_key=True, init=False)

    process_id: Mapped[int] = mapped_column(db.ForeignKey("process.id"), nullable=False)
    discipline_id: Mapped[int] = mapped_column(
        db.ForeignKey("discipline.id"), nullable=False
    )

    user_id: Mapped[int] = mapped_column(db.ForeignKey("user.id"), nullable=False)
    process: Mapped["Process"] = relationship("Process", back_populates="entities")
    discipline: Mapped["Discipline"] = relationship(
        "Discipline", back_populates="entities"
    )

    user: Mapped["User"] = relationship("User", back_populates="entities")

    @hybrid_property
    def entity_id(self):
        entity_id = "{discipline_code}-{id}".format(
            discipline_code=self.discipline.code, id=str(self.id).zfill(6)
        )
        return entity_id

    def __repr__(self):
        return f"<Entity {self.entity_id}>"


class Discipline(Base):
    __tablename__ = "discipline"
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    code: Mapped[str] = mapped_column(String(3), nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)

    entities: Mapped[List["Entity"]] = relationship(
        "Entity", back_populates="discipline", init=False
    )

    def __repr__(self):
        return f"<Discipline {self.name} ({self.code})>"


class StepInput(Base):
    __tablename__ = "step_input"
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    input_id: Mapped[int] = mapped_column(ForeignKey("input.id"), nullable=False)
    process_step_id: Mapped[int] = mapped_column(
        ForeignKey("process_step.id"), nullable=False
    )
    value: Mapped[float] = mapped_column(nullable=False)

    input: Mapped["Input"] = relationship("Input", back_populates="step_inputs")
    process_step: Mapped["ProcessStep"] = relationship(
        "ProcessStep", back_populates="step_inputs"
    )

    def __repr__(self):
        return f"<Step Input {self.id}>"


class StepParam(Base):
    __tablename__ = "step_param"
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    param_id: Mapped[int] = mapped_column(ForeignKey("param.id"), nullable=False)
    process_step_id: Mapped[int] = mapped_column(
        ForeignKey("process_step.id"), nullable=False
    )
    value: Mapped[float] = mapped_column(nullable=False)
    param: Mapped["Param"] = relationship("Param", back_populates="step_params")

    process_step: Mapped["ProcessStep"] = relationship(
        "ProcessStep", back_populates="step_params"
    )

    def __repr__(self):
        return f"<Step Param {self.id}>"


# A Process describes a process, broken up into a minimum of 1 step. A Process can be considered a recipie, this recipie is instanced for each time a Process is run. Technically we could run a Process without Entities.
class Process(Base):
    __tablename__ = "process"
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    process_date: Mapped[datetime] = mapped_column(nullable=False)

    process_steps: Mapped[List["ProcessStep"]] = relationship(
        "ProcessStep", back_populates="process", init=False
    )

    entities: Mapped[List["Entity"]] = relationship(
        "Entity", back_populates="process", init=False
    )


class ProcessStep(Base):
    __tablename__ = "process_step"
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    process_id: Mapped[int] = mapped_column(ForeignKey("process.id"), nullable=False)
    process_method_part_id: Mapped[int] = mapped_column(
        ForeignKey("process_method_part.id"), nullable=False
    )
    order: Mapped[int] = mapped_column(nullable=False)
    process: Mapped["Process"] = relationship("Process", back_populates="process_steps")

    process_method_part: Mapped["ProcessMethodPart"] = relationship(
        "ProcessMethodPart", back_populates="process_steps"
    )
    step_inputs: Mapped[List["StepInput"]] = relationship(
        "StepInput", back_populates="process_step", init=False
    )

    step_params: Mapped[List["StepParam"]] = relationship(
        "StepParam", back_populates="process_step", init=False
    )


# Method describe how a Process is carried out,
# such as using a piece of equipment or how to handle an Entity


class ProcessMethod(Base):
    __tablename__ = "process_method"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    file_name: Mapped[str] = mapped_column(nullable=False)

    process_method_parts: Mapped[List["ProcessMethodPart"]] = relationship(
        back_populates="process_method",
        init=False,
        cascade="all, delete",
    )

    def __repr__(self):
        return f"<Process Method {self.name}>"


class ProcessMethodPart(Base):
    __tablename__ = "process_method_part"
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    name: Mapped[str] = mapped_column(nullable=False)
    process_method_id: Mapped[int] = mapped_column(
        db.ForeignKey("process_method.id"), nullable=False
    )
    process_method: Mapped["ProcessMethod"] = relationship(
        back_populates="process_method_parts"
    )
    process_steps: Mapped[List["ProcessStep"]] = relationship(
        "ProcessStep", back_populates="process_method_part", init=False
    )

    def __repr__(self):
        return f"<Process Method Part {self.name}>"
