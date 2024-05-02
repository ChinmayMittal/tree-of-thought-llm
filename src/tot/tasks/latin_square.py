import os
from typing import Optional
from tot.tasks.base import Task, DATA_PATH
from tot.prompts.latin_square import * 

def clean_lines(lines: list[str]) -> list[str]:
    return [line.strip() for line in lines if line.strip()]

def input_from_text(input_text: list[str], **kwargs):
    input_text = clean_lines(input_text)
    input_board = [list(map(int, line.strip().split())) for line in input_text]
    return input_board

def output_from_text(output_text: list[str], **kwargs):
    try:
        output_text = clean_lines(output_text)
        num_lines = len(output_text)
        if num_lines == 0:
            return {
                    "OUTPUT": None,
                    "ERROR": "Output is Empty"
            }
        output_board = [list(map(int, line.strip().split())) for line in output_text]
        for row in output_board:
            if len(row) != num_lines:
                return {
                    "OUTPUT": None,
                    "ERROR": f"Each non empty row in output.txt must have {num_lines} numbers"
                }
        return {
            'OUTPUT': output_board,
            "ERROR": None
        }
    except Exception as e:
        return {
            "OUTPUT": None,
            "ERROR": f"Could not parse output.txt, output format should match description, when my script tried to parse output.txt the following exception was generated:\n{e}"
        }

def input_to_text_string(input_sample, **kwargs) -> str:
    return "\n".join(" ".join(map(str, row)) for row in input_sample)

def output_to_text_string(output_sample, **kwargs) -> str:
    return "\n".join(" ".join(map(str, row)) for row in output_sample)

def read_file(filename: str, **kwargs):
    inputs = []
    current_input = []

    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()  # Remove leading/trailing whitespace
            if not line:  # Check for blank line
                if current_input:  # If the current input is not empty, add it to the list of inputs
                    inputs.append(current_input)
                    current_input = []  # Reset the current input
            else:
                current_input.append(line)

        if current_input:  # Add the last chunk if not already added
            inputs.append(current_input)

    return inputs

class LatinSquareDataset:
    def __init__(self, input_dataset_file: str, output_dataset_file: Optional[str], **kwargs):
        self.input_dataset_file = input_dataset_file
        self.output_dataset_file = output_dataset_file
        self.outputs_present = self.output_dataset_file is not None
        self.kwargs = kwargs
        inputs = read_file(self.input_dataset_file, **kwargs)
        self.inputs = [input_from_text(input, **kwargs) for input in inputs]
        if self.outputs_present:
            outputs = read_file(self.output_dataset_file, **kwargs)
            self.outputs = [output_from_text(output, **kwargs) for output in outputs]
            assert len(self.inputs) == len(self.outputs)
    
    def __len__(self):
        return len(self.inputs)

    def __getitem__(self, idx: int):
        if idx >= len(self):
            raise IndexError(f"index: {idx} out of range for dataset of length: {len(self)}")
        return {
            "input": self.inputs[idx],
            "output": self.outputs[idx] if self.outputs_present else None
        }


class LatinSquareTask(Task):
    """
    """

    def __init__(self, file='latin-squares.txt'):
        """
        file: a csv file (fixed)
        """
        super().__init__()
        path = os.path.join(DATA_PATH, 'latin-square', file)
        self.dataset = LatinSquareDataset(path, None)
        self.value_cache = {}
        
    def __len__(self) -> int:
        return len(self.dataset)
    
    def get_input(self, idx: int) -> str:
        return input_to_text_string(self.dataset[idx]['input'])
    
    @staticmethod
    def get_max_depth(input_board: str) -> int:
        return input_board.count('0')
    
    @staticmethod
    def propose_prompt_wrap(node: str) -> str:
        return propose_prompt.format(input=node)
    
    @staticmethod
    def value_prompt_wrap(node: str) -> str:
        return value_prompt.format(input=node)
    
    @staticmethod
    def value_outputs_unwrap(value_outputs: list) -> float:
        value_names = [value_output.split("\n")[-1].strip().lower() for value_output in value_outputs]
        value_map = {'impossible': 0.001, 'likely': 1, 'sure': 20}  # TODO: ad hoc
        value = sum(value * value_names.count(name) for name, value in value_map.items())/len(value_names)
        return value
        


