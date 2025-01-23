"""Contains sqlalchemy models for the process_navigator app."""

from typing import List

from sqlalchemy import DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String
from sqlalchemy.ext.hybrid import hybrid_property


from process_navigator.extensions.database import Base, db


# Define the models for the database
# an Entity represents a physical object that can be isolated and analysed. This is up to some interpretation by the user
class Entity(Base):
    __tablename__ = "entity"
    id: Mapped[int] = mapped_column(primary_key=True, init=False)

    process_instance_id: Mapped[int] = mapped_column(
        db.ForeignKey("process_instance.id"), nullable=False
    )
    discipline_id: Mapped[int] = mapped_column(
        db.ForeignKey("discipline.id"), nullable=False
    )

    user_id: Mapped[int] = mapped_column(db.ForeignKey("user.id"), nullable=False)
    process_instance: Mapped["ProcessInstance"] = relationship(
        "ProcessInstance", back_populates="entities"
    )
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


class InputValue(Base):
    __tablename__ = "input_value"
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    input_id: Mapped[int] = mapped_column(db.ForeignKey("input.id"), nullable=False)
    value: Mapped[float] = mapped_column(nullable=False)
    input: Mapped["Input"] = relationship(
        "Input", back_populates="input_values", init=False
    )
    step_input_values: Mapped[List["StepInputValue"]] = relationship(
        "StepInputValue", back_populates="input_value", init=False
    )

    def __repr__(self):
        return f"<Input Value {self.value}>"


class ParamValue(Base):
    __tablename__ = "param_value"
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    param_id: Mapped[int] = mapped_column(db.ForeignKey("param.id"), nullable=False)
    value: Mapped[float] = mapped_column(nullable=False)
    param: Mapped["Param"] = relationship(
        "Param", back_populates="param_values", init=False
    )
    step_param_values: Mapped[List["StepParamValue"]] = relationship(
        "StepParamValue", back_populates="param_value", init=False
    )

    def __repr__(self):
        return f"<Param Value {self.value}>"


class StepInputValue(Base):
    __tablename__ = "step_input_value"
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    step_id: Mapped[int] = mapped_column(ForeignKey("step.id"), nullable=False)
    input_value_id: Mapped[int] = mapped_column(
        ForeignKey("input_value.id"), nullable=False
    )
    input_value: Mapped["InputValue"] = relationship(
        "InputValue", back_populates="step_input_values"
    )
    step: Mapped["Step"] = relationship("Step", back_populates="step_input_values")

    def __repr__(self):
        return f"<Step Input Value {self.id}>"


class StepParamValue(Base):
    __tablename__ = "step_param_value"
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    step_id: Mapped[int] = mapped_column(ForeignKey("step.id"), nullable=False)
    param_value_id: Mapped[int] = mapped_column(
        ForeignKey("param_value.id"), nullable=False
    )
    param_value: Mapped["ParamValue"] = relationship(
        "ParamValue", back_populates="step_param_values"
    )
    step: Mapped["Step"] = relationship("Step", back_populates="step_param_values")

    def __repr__(self):
        return f"<Step Param Value {self.id}>"


"""
Each Step is unique combination of InputValue, ParamValues and ProcessMethodParts. Therefore each step can be reused.
"""


class Step(Base):
    __tablename__ = "step"
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    process_method_part_id: Mapped[int] = mapped_column(
        ForeignKey("process_method_part.id"), nullable=False
    )
    process_method_part: Mapped["ProcessMethodPart"] = relationship(
        "ProcessMethodPart", back_populates="steps"
    )

    step_input_values: Mapped[List["StepInputValue"]] = relationship(
        "StepInputValue", back_populates="step"
    )
    step_param_values: Mapped[List["StepParamValue"]] = relationship(
        "StepParamValue", back_populates="step"
    )

    process_steps: Mapped[List["ProcessStep"]] = relationship(
        "ProcessStep", back_populates="step", init=False
    )

    def __repr__(self):
        return f"<Step {self.id}>"


# each Entity is descibed by a single Process instance. A Process Instance can link to multiple entities, this providing 'sibling' Entities
class ProcessInstance(Base):
    __tablename__ = "process_instance"
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    process_id: Mapped[int] = mapped_column(ForeignKey("process.id"), nullable=False)
    process_date: Mapped[str] = mapped_column(DateTime, nullable=False)

    entities: Mapped[List["Entity"]] = relationship(
        "Entity", back_populates="process_instance", init=False
    )


# A Process describes a process, broken up into a minimum of 1 step. A Process can be considered a recipie, this recipie is instanced for each time a Process is run. Technically we could run a Process without Entities.
class Process(Base):
    __tablename__ = "process"
    id: Mapped[int] = mapped_column(primary_key=True, init=False)

    process_steps: Mapped[List["ProcessStep"]] = relationship(
        "ProcessStep", back_populates="process"
    )


class ProcessStep(Base):
    __tablename__ = "process_step"
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    process_id: Mapped[int] = mapped_column(ForeignKey("process.id"), nullable=False)
    step_id: Mapped[int] = mapped_column(ForeignKey("step.id"), nullable=False)
    order: Mapped[int] = mapped_column(nullable=False)
    process: Mapped["Process"] = relationship("Process", back_populates="process_steps")
    step: Mapped["Step"] = relationship("Step", back_populates="process_steps")

    __table_args__ = (
        UniqueConstraint(
            "process_id", "order", "step_id", name="unique_process_step_order"
        ),
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
    steps: Mapped[List["Step"]] = relationship(
        "Step", back_populates="process_method_part", init=False
    )

    def __repr__(self):
        return f"<Process Method Part {self.name}>"
