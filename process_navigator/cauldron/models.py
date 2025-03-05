from .forms import (
    ProcessPathForm,
    ProcessForm,
    ProcessStepForm,
    ParametersForm,
    InputsForm,
)
from itertools import product
import copy
import datetime
from dataclasses import dataclass
from typing import List
from process_navigator.models.process import Process, ProcessStep, StepParam, StepInput
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
        self.processes = []


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

    # each time this function is called it should map out each possible path, ready to used a template for the database
    def generate_paths(self):
        for process in self.form.processes:
            self._generate_process(process)

            for step_index, step in enumerate(process.process_steps, start=1):
                self._generate_step(step, step_index)

                # now we check if there are multiple values for the parameters and inputs and expand the paths accordingly
                for parameter_index, parameter in enumerate(step.parameters):
                    if len(parameter.values) > 1:
                        self._expand_paths(parameter, "parameter")

    def _generate_process(self, process: ProcessForm):
        # so the HoldingProcess needs to be created and added to each Path before we add the steps
        # this due to the need to expand the paths based on multiple values
        # this will be the same with the HoldingProcessStep and params/inputs.
        # we just need to reference the last [-1] when appending

        new_process = HoldingProcess(
            process_date=process.process_date.data, process_steps=[]
        )

        for path in self.paths:
            path.processes.append(new_process)

    def _generate_step(self, step: ProcessStepForm, order: int):
        new_step = HoldingProcessStep(
            process_method_part_id=step.process_method_part.data.id,
            order=order,
            step_params=[],
            step_inputs=[],
        )

        for path in self.paths:
            last_process = path.processes[-1]
            last_process.process_steps.append(new_step)

    def _generate_step_parameter(self, parameter: ParametersForm):
        return HoldingStepParam(
            param_id=parameter.parameter.data.id,
            value=parameter.values[0].value.data,
        )

    def _generate_step_input(self, input: InputsForm):
        return HoldingStepInput(
            input_id=input.input.data.id, value=input.values[0].value.data
        )

    def _copy_path(self, path: Path):
        new_path = path
        return new_path


# this class deals with commit the data to the database
# for Process and Process Steps there are no multiple value options
# for Inputs and Parametes, as we come across multiple values we will need to copy Path objects
# however, this is complicated by the fact that each object will have an id generated by the database
class PathCommit:
    def __init__(self, form: ProcessPathForm):
        self.form = form

        # start off with one empty Path object
        self.paths = [Path()]

    def generate_db_objects(self):
        # for each path, we generate the Process and Process Steps.
        # the Path object gets passed through and Processes appended to it
        # The sqlalchemy Process object will keep all the Process Steps and other process information
        for path_index, path in enumerate(self.paths):
            print("starting path: ", path_index)
            for process in self.form.processes:
                self._generate_process(process, path)
            print("finished path: ", path_index)

    def _generate_process(self, process: ProcessForm, path: Path):
        print("generating process")
        new_process = Process(process_date=process.process_date.data)
        db.session.add(new_process)
        db.session.commit()

        print("new process id: ", new_process.id, " added to database")

        # add to the Path object
        path.processes.append(new_process)

        for step_index, step in enumerate(process.process_steps, start=1):
            self._generate_step(new_process, step, step_index)

    def _generate_step(self, process: Process, step: ProcessStepForm, order: int):
        print("generating step")
        new_step = ProcessStep(
            process_id=process.id,
            process_method_part_id=step.process_method_part.data.id,
            order=order,
            process=process,
            process_method_part=step.process_method_part.data,
        )

        db.session.add(new_step)
        db.session.commit()

        print("new step id: ", new_step.id, " added to database")
        # this will cycle through the paarameters for each step
        # there will be a check to see if multiple values are present, if so then copies of the Path object need to be made
        for parameter_index, parameter in enumerate(step.parameters):
            # check for multiple values:
            if len(parameter.values) > 1:
                print("multiple values found")
                # this bit is conceptually a bit tricky
                # we need to capture the state of the current paths
                # for the first value of the multiiple values, we will directly modify the path
                # however, for the subsequent values, we will copy the paths and then use those as copy templates
                # if we don't do this, we will end up with a lot of duplicate data as the first and n value will be added to the path

                # deep copy was initially used, but this was causing issues with the database as the objects became detached from the Session
                # this could be fixed by just passing through the data but copy.copy will be tried first
                print("attempting a copy of paths")
                capture_path_state = copy.deepcopy(self.paths)
                print("current number of paths: ", len(self.paths))
                for value_index, value in enumerate(parameter.values):
                    # for the first value, we don't need to copy the path
                    if value_index == 0:
                        print("no copies needed for first value")
                        self._generate_step_parameter(
                            parameter, new_step, value_index=value_index
                        )
                    else:
                        for path in capture_path_state:
                            print(
                                "this copied path has:",
                                len(path.processes),
                                "processes",
                            )
                            new_path = self._copy_path(path)

                            # get the last process step of the last process in the path
                            last_process = new_path.processes[-1]
                            last_step = last_process.process_steps[-1]
                            # add the new parameter to the new path
                            self._generate_step_parameter(
                                parameter, last_step, value_index=value_index
                            )
                    print("current number of paths after values: ", len(self.paths))

            else:
                print("no multiple values found")
                self._generate_step_parameter(parameter, new_step, value_index=0)
                print("current number of paths after values: ", len(self.paths))

        for input_index, input in enumerate(step.inputs):
            self._generate_step_input(input, new_step, input_index)

    def _generate_step_parameter(
        self, parameter: ParametersForm, step: ProcessStep, value_index: int
    ):
        print("generating step parameter")
        value = parameter.values[value_index].value.data
        new_step_parameter = StepParam(
            param_id=parameter.parameter.data.id,
            process_step_id=step.id,
            value=value,
            param=parameter.parameter.data,
            process_step=step,
        )

        db.session.add(new_step_parameter)
        db.session.commit()

        print("new parameter of value: ", value, " added to database")

    def _generate_step_input(
        self, input: InputsForm, step: ProcessStep, value_index: int
    ):
        value = input.values[value_index].value.data
        new_step_input = StepInput(
            input_id=input.input.data.id,
            process_step_id=step.id,
            value=value,
            input=input.input.data,
            process_step=step,
        )
        db.session.add(new_step_input)
        db.session.commit()

        print("new input of value: ", value, " added to database")

    def _copy_path(self, path: Path):
        print("copying path")
        new_path = Path()
        for process in path.processes:
            print("copying process: ", process.id)
            new_process = self._copy_process(process.__dict__)
            new_path.processes.append(new_process)

        print("path copied")
        return new_path

    def _copy_process(self, process_to_copy: Process):
        print("copying process")
        print("process to copy id: ", process_to_copy)
        new_process = Process(
            process_date=process_to_copy.process_date,
        )
        print("attempting to add new process to database")
        db.session.add(new_process)
        db.session.commit()

        for process_step in process_to_copy.process_steps:
            self._copy_process_step(process_step, process=new_process)

        print("process copied")
        return new_process

    def _copy_process_step(self, process_step_to_copy: ProcessStep, process: Process):
        print("copying process step")
        new_process_step = ProcessStep(
            process_id=process_step_to_copy.process_id,
            process_method_part_id=process_step_to_copy.process_method_part_id,
            order=process_step_to_copy.order,
            process=process,
            process_method_part=process_step_to_copy.process_method_part,
        )
        db.session.add(new_process_step)
        db.session.commit()

        # copy the step parameters
        for step_param in process_step_to_copy.step_params:
            self._copy_step_param(step_param, process_step=new_process_step)

        # copy the step inputs
        for step_input in process_step_to_copy.step_inputs:
            self._copy_step_input(step_input, process_step=new_process_step)

        print("process step copied")

    def _copy_step_param(
        self, step_param_to_copy: StepParam, process_step: ProcessStep
    ):
        new_step_param = StepParam(
            param_id=step_param_to_copy.param_id,
            process_step_id=process_step.id,
            value=step_param_to_copy.value,
            param=step_param_to_copy.param,
            process_step=process_step,
        )
        db.session.add(new_step_param)
        db.session.commit()

    def _copy_step_input(
        self, step_input_to_copy: StepInput, process_step: ProcessStep
    ):
        new_step_input = StepInput(
            input_id=step_input_to_copy.input_id,
            process_step_id=process_step.id,
            value=step_input_to_copy.value,
            input=step_input_to_copy.input,
            process_step=process_step,
        )
        db.session.add(new_step_input)
        db.session.commit()
