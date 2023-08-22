# User Search Auto-Complete Tool

This tool provides auto-complete suggestions based on user search input. It uses a self-developed suggestion algorithm
that can handle a mismatch of one character.

## Algorithms and Data Structures

The tool uses the following data structures and algorithms:

- `FileData` Class:
    - `data_dict`: A dictionary where the key is a unique integer assigned to each file and the value is a tuple of the
      file's name and a list of the file's content.
    - `words_graph`: A dictionary where the key is a word and the value is a list of objects that contain information
      about the location of the word's appearances in the files, such as the file number and row number.

- Suggestion Algorithm: A self-developed algorithm that finds the top five suggestions to show to the user based on the
  user's input.

## Detailed Code Flow

The tool works as follows:

1. The files are uploaded into the dictionary.
2. The mapping for each word is applied to all the sentences it appears in.
3. For each user input, the suggestion algorithm is used to find the top five suggestions to show to the user.

## Getting Started

To get started with the tool, you can follow these steps:

1. **Clone the project from GitHub:**

> https://github.com/Lev-Excellenteam-2023/google-google-project-group-02.git

2. **Install the required packages using the following command:**

> pip install -r requirements.txt

3. **Set up a path to the archive folder:**

- Create a `.env` file in the top-level directory of the project.
- In the `.env` file, add the following line:
  ```
  ARCHIVE_FOLDER_PATH = "C:\\###\\google-project-group-02\\Archive"
  ```
  Replace `###` with the correct path to the project on your PC.
  Alternatively, you can add an environment variable in your system called `ARCHIVE_FOLDER_PATH` and set its value to
  the path to the archive folder in the project.

You are now all set to use the tool!

