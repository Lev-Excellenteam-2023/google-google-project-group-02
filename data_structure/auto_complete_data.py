from dataclasses import dataclass


@dataclass
class AutoCompleteData:
    completed_sentence: str
    file_name: str
    line_number: int

    def __str__(self):
        return self.completed_sentence + f"({self.file_name} {self.line_number})"
