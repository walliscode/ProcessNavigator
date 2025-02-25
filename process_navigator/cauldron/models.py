from .forms import ProcessPathForm
from itertools import product


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
