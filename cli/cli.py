import datetime
import logging
import os
from os import environ, path
from util.consts import CLI_WELCOME_MESSAGE, INPUT_MESSAGE, ROW_CONTENT, FILE_NUMBER, ROW_NUMBER, FILE_NAME,\
    RESET_SYMBOL, BOOT_MESSAGE
from util.remove_punctuation_util import process_sentence
from data_structure.file_data import FileData
from suggest_engine.suggest import find_top_five_completions
from data_structure.auto_complete_data import AutoCompleteData
from typing import List
from time import time


def get_best_k_completions(prefix: str, data_cache: FileData) -> List[AutoCompleteData]:
    """
    return five best suggestions matching a user input.
    :param prefix: user input to find suggestions for.
    :param data_cache: dictionary mapping a file number, to its content split into lines.
    :return: list of five AutoCompleteData objects, each containing a suggestion line and metadata about it.
    """
    processed_prefix = process_sentence(prefix)
    suggestions_metadata = find_top_five_completions(processed_prefix, data_cache)

    processed_suggestions = []
    for suggestion in suggestions_metadata:
        line_content = suggestion[ROW_CONTENT]
        file_name = data_cache.data_dict[suggestion[FILE_NUMBER]][FILE_NAME][:-4]
        row_number = suggestion[ROW_NUMBER] + 1
        processed_suggestions.append(AutoCompleteData(line_content, file_name, row_number))

    return processed_suggestions


def print_results(result_list: List[AutoCompleteData]) -> None:
    for result in result_list:
        print(result)
    print()


def configure_environment() -> str:
    """
    configure and return the path to archive folder to upload to the FileData object
    :return: path to the folder
    """
    try:
        # attempt to use .env file
        import dotenv
        if path.exists(r"..\.env"):
            dotenv.load_dotenv()
            return environ.get("ARCHIVE_FOLDER_PATH")
    except ImportError as e:
        pass  # todo - add logg instead

    return environ.get("ARCHIVE_FOLDER_PATH")


def read_input_from_user(old_input: str = "") -> str:
    print(INPUT_MESSAGE)
    print(old_input, end="")
    user_input: str = str(input())
    return user_input


def requested_reset(user_input: str) -> bool:
    """
    check if user wants to end current search and reset (input == #)
    :param user_input:current user input
    :return: bool
    """
    if user_input == RESET_SYMBOL:
        return True
    else:
        return False


def main():
    uploaded_files_cache = FileData(configure_environment())
    print(CLI_WELCOME_MESSAGE)
    prev_user_input: str = ""
    while True:
        user_input = read_input_from_user(prev_user_input)
        prev_user_input += user_input
        if not requested_reset(user_input):
            logging.info(f"User Input: {prev_user_input}")

            start_time = time()
            suggested_lines = get_best_k_completions(prev_user_input, uploaded_files_cache)
            end_time = time()

            print_results(suggested_lines)
            logging.info(f"Suggested Lines: {suggested_lines}")

            execution_time = end_time - start_time
            logging.debug(f"Execution Time: {execution_time} seconds\n")

        else:
            prev_user_input = ""


if __name__ == "__main__":
    print(BOOT_MESSAGE)
    log_file_path = os.path.join("../logs", 'suggestions_logfile.log')
    logging.basicConfig(filename=log_file_path, level=logging.DEBUG)
    logging.info(f"Script started at: {datetime.datetime.now()}")
    main()
