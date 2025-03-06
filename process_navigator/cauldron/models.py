from .forms import (
    ProcessPathForm,
    ProcessForm,
    ProcessStepForm,
    ParametersForm,
    InputsForm,
)
from itertools import product
from copy import deepcopy
import datetime
from dataclasses import dataclass
from typing import List
from process_navigator.models.process import (
    Process,
    ProcessStep,
    StepParam,
    StepInput,
    ProcessMethodPart,
)
from process_navigator.models.parameters import Param
from process_navigator.models.inputs import Input
from process_navigator.extensions.database import db


# this class deals with presenting the data to the user
# namely, about their current Cauldron configuration
# E.g. if they pick to multiple variable values, they will have multiple paths
# or it they repeat a particaular process, they will have multiple entities
class PathData:
    def __init__(self, form: ProcessPathForm):
        self.form = form
        self.number_of_processes = len(form.processes)
        self.paths = self.expand_paths()
        self.number_of_paths = len(self.paths)

    def expand_paths(self):
        all_combinations = []
        for process in self.form.processes:
            process_combinations = self._expand_process(process)
            all_combinations.append(process_combinations)

        # Generate all combinations of processes
        expanded_paths = list(product(*all_combinations))
        return expanded_paths

    def _expand_process(self, process):
        step_combinations = []

        # collate all expanded step combinations
        for step in process.process_steps:
            step_combinations.append(self._expand_step(step))

        # Generate all combinations of steps within a process
        process_combinations = list(product(*step_combinations))
        return process_combinations

    def _expand_step(self, step):
        # get all inputs within a step and get their product
        input_combinations = self._calculate_combinations(step.inputs)

        # get all parameters within a step and get their product
        parameter_combinations = self._calculate_combinations(step.parameters)

        # Generate all combinations of inputs and parameters within a step
        step_combinations = list(product(input_combinations, parameter_combinations))
        return step_combinations

    def _calculate_combinations(self, items):
        if not items:
            return [()]
        return list(product(*[item.values for item in items]))


class Path:
    def __init__(self):
        self.processes: List[HoldingProcess] = []


@dataclass
class HoldingStepParam:
    param_id: int
    value: float


@dataclass
class HoldingStepInput:
    input_id: int
    value: float


@dataclass
class HoldingProcessStep:
    process_method_part_id: int
    order: int
    step_params: List[HoldingStepParam]
    step_inputs: List[HoldingStepInput]


@dataclass
class HoldingProcess:
    process_date: datetime.datetime
    process_steps: List[HoldingProcessStep]


class HoldingPath:
    def __init__(self, form: ProcessPathForm):
        self.form = form
        self.paths = [Path()]
        self.generate_paths()
        self.number_of_paths = len(self.paths)

    # each time this function is called it should map out each possible path, ready to used a template for the database
    def generate_paths(self):
        for process in self.form.processes:
            self._generate_process(process)  # type: ignore

            for step_index, step in enumerate(process.process_steps, start=1):  # type: ignore
                self._generate_step(step, order=step_index)

                # now we check if there are multiple values for the parameters and inputs and expand the paths accordingly
                for parameter in step.parameters:
                    if len(parameter.values) > 1:
                        freeze_current_paths = deepcopy(self.paths)

                        for value_index, value in enumerate(parameter.values):
                            new_parameter = self._generate_step_parameter(
                                parameter, value_index
                            )

                            if value_index == 0:
                                for path in self.paths:
                                    last_process = path.processes[-1]

                                    last_step = last_process.process_steps[-1]

                                    last_step.step_params.append(new_parameter)

                            else:
                                for path in freeze_current_paths:
                                    new_path = self._copy_path(path)
                                    last_process = new_path.processes[-1]
                                    last_step = last_process.process_steps[-1]

                                    last_step.step_params.append(new_parameter)

                                    self.paths.append(new_path)

                    # multiple values not present so we assign to all paths
                    else:
                        print("only one value present for this parameter")
                        new_parameter = self._generate_step_parameter(parameter, 0)
                        for path in self.paths:
                            last_process = path.processes[-1]
                            last_step = last_process.process_steps[-1]
                            last_step.step_params.append(new_parameter)

                for input in step.inputs:
                    if len(input.values) > 1:
                        print("there are " + str(len(input.values)) + " input values")
                        freeze_current_paths = deepcopy(self.paths)
                        print(
                            "starting length of freeze_current_paths",
                            len(freeze_current_paths),
                        )
                        for value_index, value in enumerate(input.values):
                            if value_index == 0:
                                new_input = self._generate_step_input(
                                    input, value_index
                                )
                                print("there are " + str(len(self.paths)) + " paths")
                                for path in self.paths:
                                    last_process = path.processes[-1]
                                    last_step = last_process.process_steps[-1]
                                    print(
                                        "this process currently has "
                                        + str(len(last_step.step_inputs))
                                        + " inputs"
                                    )
                                    last_step.step_inputs.append(new_input)
                            else:
                                for path in freeze_current_paths:
                                    new_path = self._copy_path(path)
                                    last_process = new_path.processes[-1]
                                    last_step = last_process.process_steps[-1]
                                    new_input = self._generate_step_input(
                                        input, value_index=value_index
                                    )
                                    last_step.step_inputs.append(new_input)
                                    self.paths.append(new_path)

                    # multiple values not present so we assign to all paths
                    else:
                        new_input = self._generate_step_input(input, value_index=0)
                        for path in self.paths:
                            last_process = path.processes[-1]
                            last_step = last_process.process_steps[-1]
                            last_step.step_inputs.append(new_input)

    def _generate_process(self, process: ProcessForm):
        # so the HoldingProcess needs to be created and added to each Path before we add the steps
        # this due to the need to expand the paths based on multiple values
        # this will be the same with the HoldingProcessStep and params/inputs.
        # we just need to reference the last [-1] when appending

        for path in self.paths:
            # a new HolingProcess needs to be created for each Path, otherwise the same object is referenced
            new_process = HoldingProcess(
                process_date=process.process_date.data,  # type: ignore
                process_steps=[],  # type: ignore
            )
            path.processes.append(new_process)

    def _generate_step(self, step: ProcessStepForm, order: int):
        for path in self.paths:
            new_step = HoldingProcessStep(
                process_method_part_id=step.process_method_part.data.id,
                order=order,
                step_params=[],
                step_inputs=[],
            )

            last_process = path.processes[-1]
            last_process.process_steps.append(new_step)

    def _generate_step_parameter(self, parameter: ParametersForm, value_index: int):
        return HoldingStepParam(
            param_id=parameter.parameter.data.id,
            value=parameter.values[value_index].value.data,
        )

    def _generate_step_input(self, input: InputsForm, value_index: int):
        return HoldingStepInput(
            input_id=input.input.data.id, value=input.values[value_index].value.data
        )

    def _copy_path(self, path_to_copy: Path):
        new_path = Path()

        for process in path_to_copy.processes:
            new_process = HoldingProcess(
                process_date=process.process_date,
                process_steps=[
                    HoldingProcessStep(
                        process_method_part_id=step.process_method_part_id,
                        order=step.order,
                        step_params=[
                            HoldingStepParam(param_id=param.param_id, value=param.value)
                            for param in step.step_params
                        ],
                        step_inputs=[
                            HoldingStepInput(input_id=input.input_id, value=input.value)
                            for input in step.step_inputs
                        ],
                    )
                    for step in process.process_steps
                ],
            )
            new_path.processes.append(new_process)

        return new_path

    def to_dict(self):
        return {
            "number_of_paths": self.number_of_paths,
            "paths": [
                {
                    "processes": [
                        {
                            "process_date": process.process_date,
                            "process_steps": [
                                {
                                    "process_method_part_id": step.process_method_part_id,
                                    "order": step.order,
                                    "step_params": [
                                        {
                                            "param_id": param.param_id,
                                            "value": param.value,
                                        }
                                        for param in step.step_params
                                    ],
                                    "step_inputs": [
                                        {
                                            "input_id": input.input_id,
                                            "value": input.value,
                                        }
                                        for input in step.step_inputs
                                    ],
                                }
                                for step in process.process_steps
                            ],
                        }
                        for process in path.processes
                    ]
                }
                for path in self.paths
            ],
        }


# this class will take in a HoldingPath object and when the commit methods is called it will commit the data to the database
#
class PathCommit:
    def __init__(self, paths: HoldingPath):
        self.all_combinations = paths

    def commit_data(self):
        for path in self.all_combinations.paths:
            self._commit_path(path)

    def _commit_path(self, path: Path):
        for process in path.processes:
            self._commit_process(process)

    def _commit_process(self, process: HoldingProcess):
        new_process = Process(process_date=process.process_date)
        db.session.add(new_process)
        db.session.commit()

        for step in process.process_steps:
            self._commit_step(step, new_process)

    def _commit_step(self, holding_step: HoldingProcessStep, process: Process):
        process_method_part_query = db.session.execute(
            db.select(ProcessMethodPart).filter(
                ProcessMethodPart.id == holding_step.process_method_part_id
            )
        ).scalar_one()
        new_step = ProcessStep(
            process_method_part_id=holding_step.process_method_part_id,
            order=holding_step.order,
            process_id=process.id,
            process=process,
            process_method_part=process_method_part_query,
        )
        db.session.add(new_step)
        db.session.commit()
        for param in holding_step.step_params:
            self._commit_param(param, new_step)
        for input in holding_step.step_inputs:
            self._commit_input(input, new_step)

    def _commit_param(self, param: HoldingStepParam, step: ProcessStep):
        param_query = db.session.execute(
            db.select(Param).filter(Param.id == param.param_id)
        ).scalar_one()
        new_param = StepParam(
            param_id=param.param_id,
            value=param.value,
            process_step_id=step.id,
            process_step=step,
            param=param_query,
        )
        db.session.add(new_param)
        db.session.commit()

    def _commit_input(self, input: HoldingStepInput, step: ProcessStep):
        input_query = db.session.execute(
            db.select(Input).filter(Input.id == input.input_id)
        ).scalar_one()
        new_input = StepInput(
            input_id=input.input_id,
            value=input.value,
            process_step_id=step.id,
            process_step=step,
            input=input_query,
        )
        db.session.add(new_input)
        db.session.commit()
