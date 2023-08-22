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
1. **Uploading Files and Data Dictionary Creation:**
   Files are seamlessly uploaded into the `data_dict` dictionary. Each file is assigned a unique integer key for easy reference. The corresponding value for each key is a list that includes the file name and its content, divided into rows.


2. **Mapping Words for Contextual Data:**
   During the iteration of content within the `data_dict`, a word mapping process is initiated. With every occurrence of a word throughout the sentences, a corresponding `WordData` object is generated. This `WordData` object holds essential details like the file number, row number, and the word's position within the sentence. For each instance of a word being cited in the files, a `WordData` object is appended to a dedicated list associated with that specific word. Consequently, this dynamic mapping employs the words themselves as keys, with their associated lists of `WordData` objects serving as the corresponding values.


3. **Suggestion Algorithm for User Input:**
   Whenever a user provides input, a suggestion algorithm kicks in, generating the top five recommendations to present back to the user. The algorithm initiates by inspecting the first word of the input. It promptly checks whether this word is present within the `data_dict`. If a match is found, the algorithm retrieves the highest-scoring sentences in which the word occurs. Conversely, if the word is absent or found in fewer than five sentences, the algorithm compensates by generating suggestions for words that can be formed with a single error. This step ensures a thorough suggestion coverage for the user's needs.


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

