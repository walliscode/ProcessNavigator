""" Contains sqlalchemy models for the process_navigator app. """

from process_navigator.extensions import db


# Define the models for the database
# an Entity represents a physical object that can be isolated and analysed. This is up to some interpretation by the user
class Entity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    entityID = db.Column(db.String(10), nullable=False)
    process_instance_id = db.Column(
        db.Integer, db.ForeignKey("process_instance.id"), nullable=False
    )
    process_instance = db.relationship(
        "ProcessInstance", backref=db.backref("entities", lazy=True)
    )

    def __repr__(self):
        return f"<Entity {self.entityID}>"


# each Entity is descibed by a single Process instance. A Process Instance can link to multiple entities, this providing 'sibling' Entities
class ProcessInstance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    process_id = db.Column(db.Integer, db.ForeignKey("process.id"), nullable=False)
    process = db.relationship(
        "Process", backref=db.backref("process_instances", lazy=True)
    )
    process_date = db.Column(db.DateTime, nullable=False)


# A Process describes a process, broken up into a minimum of 1 step. A Process can be considered a recipie, this recipie is instanced for each time a Process is run. Technically we could run a Process without Entities.
class Process(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    alias = db.Column(db.String(100), nullable=True)


# each Step describes a way to combine Inputs, Parameters and Method Parts including any quantities associated. Each Step is unique thus any unique combination of Inputs, Parameters and Method Parts will be a new Step
class Step(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    method_part_id = db.Column(
        db.Integer, db.ForeignKey("method_part.id"), nullable=False
    )
    method_part = db.relationship("MethodPart", backref=db.backref("step", lazy=True))

    def __repr__(self):
        return f"<Step {self.id}>"


# Linking Process containers to Process Steps.
# This is a many to many relationship as a Process
# can have many Steps and a Step can be used in many Processes
class ProcessSteps(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    process_id = db.Column(db.Integer, db.ForeignKey("process.id"), nullable=False)
    process = db.relationship("Process", backref=db.backref("process_steps", lazy=True))
    step_id = db.Column(db.Integer, db.ForeignKey("step.id"), nullable=False)
    step = db.relationship("Step", backref=db.backref("process_steps", lazy=True))

    def __repr__(self):
        return f"<ProcessSteps {self.id}>"


# Method describe how a Process is carried out,
# such as using a piece of equipment or how to handle an Entity


class Method(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Method {self.name}>"


# The Method is broken down into method parts to describe different steps in the process.
# This is a one to many relationship as a Method can have many Method Parts
# but a Method Part can only belong to one Method
class MethodPart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    method_id = db.Column(db.Integer, db.ForeignKey("method.id"), nullable=False)
    method = db.relationship("Method", backref=db.backref("method_part", lazy=True))

    def __repr__(self):
        return f"<MethodPart {self.name}>"


class Param(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    unit_id = db.Column(db.Integer, db.ForeignKey("unit.id"), nullable=False)

    def __repr__(self):
        return f"<Param {self.name}>"


class Input(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    unit_id = db.Column(db.Integer, db.ForeignKey("unit.id"), nullable=False)

    def __repr__(self):
        return f"<Input {self.name}>"


class Unit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    symbol = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f"<Unit {self.name}>"


class StepInput(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    step_id = db.Column(db.Integer, db.ForeignKey("step.id"), nullable=False)
    step = db.relationship("Step", backref=db.backref("step_input", lazy=True))
    input_id = db.Column(db.Integer, db.ForeignKey("input.id"), nullable=False)
    input = db.relationship("Input", backref=db.backref("step_input", lazy=True))
    value = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<StepInput {self.id}>"


class StepParam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    step_id = db.Column(db.Integer, db.ForeignKey("step.id"), nullable=False)
    step = db.relationship("Step", backref=db.backref("step_param", lazy=True))
    param_id = db.Column(db.Integer, db.ForeignKey("param.id"), nullable=False)
    param = db.relationship("Param", backref=db.backref("step_param", lazy=True))
    value = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<StepParam {self.id}>"
