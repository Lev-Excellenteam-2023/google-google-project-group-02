from dataclasses import dataclass


@dataclass
class AutoCompleteData:
    """
    Represents a completed sentence with the file name and row.

    Attributes:
        completed_sentence (str): The completed sentence.
        file_name (str): The name of the file where the sentence is found.
        line_number (int): The line number in the file where the sentence is located.
    """
    completed_sentence: str
    file_name: str
    line_number: int

    def __str__(self):
        return self.completed_sentence + f"({self.file_name} {self.line_number})"
