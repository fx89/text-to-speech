# Copyright 2026 Catalin Ioan Georgescu
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# ===============================================================================
#
# Name: text_to_speech/input_text.py
#
# Description:
# Deserializes and validates input text files for text-to-speech conversion
#
# ===============================================================================

from text_to_speech.exceptions import InputTextFormatError

# ===============================================================================

class InputText:
    """
    Describes a set of paragraphs that are all part of the same input file
    """

    def __init__(self, input_paragraphs):
        self.input_paragraphs = input_paragraphs

    def get_paragraphs(self):
        return self.input_paragraphs


class InputParagraph:
    def __init__(self, actor_id, text):
        self.actor_id = actor_id
        self.text = text


# ===============================================================================

def read_input_text_file(input_text_file_path):
    # At the beginning of the file, the array of input paragraphs
    # read from the file is empty
    input_paragraphs = []

    # At the beginning of the file, there is no last actor ID
    last_actor_id = None

    # At the beginning of the file, the last line of text read
    # from the file is empty
    last_line = ""

    # Read the file line by line
    with open(input_text_file_path, 'r') as file:
        # Line counter
        line_counter = 0

        for line in file:
            # Increment the line counter
            line_counter += 1

            # Strip the line
            line = line.strip()

            # Ignore empty lines
            if not line:
                continue

            # Parse the line
            while True:
                # Look for an actor occurrence
                actor_occurrence_index = line.find("{{")

                # If there is no actor occurrence, then add the text to the last line
                if actor_occurrence_index == -1:
                    last_line += " " + line.strip()
                    break
                # If there is an actor occurrence, then switch to the new actor and
                # create the new input paragraph
                else:
                    # Add the text that can be found prior to the actor label to the
                    # last read line
                    additional_text = line[:actor_occurrence_index]
                    last_line += " " + additional_text.strip()

                    # Strip the last line
                    stripped_last_line = last_line.strip()

                    # If the stripped last line is not empty, then
                    # attempt to create an input paragraph from it
                    if stripped_last_line != "":
                        # Check if there's an actor defined and,
                        # if not, then raise an exception
                        if last_actor_id is None:
                            raise InputTextFormatError(
                                "Input text file should start with an actor label"
                            )

                        # Create and add an input paragraph for the last read actor ID
                        # and the line of text read until now
                        input_paragraphs.append(
                            InputParagraph(last_actor_id, stripped_last_line)
                        )

                        # Reset the last line
                        last_line = ""

                    # Remove the already processed part from the line
                    line = line[actor_occurrence_index + 2:]

                    # Look for the end of the actor label
                    actor_occurrence_end_index = line.find("}}")

                    # If the end of the actor label is not found, then
                    # raise an exception
                    if actor_occurrence_end_index == -1:
                        raise InputTextFormatError(
                            "Error at line " + str(line_counter) + ": " +
                            "Missing }} at the end of the actor label"
                        )

                    # Extract the actor id
                    last_actor_id = line[:actor_occurrence_end_index]

                    # Remove the already processed part from the line
                    line = line[actor_occurrence_end_index + 2:]

        # After the file is done parsing, add the last paragraph,
        # but not if it's empty
        stripped_last_line = last_line.strip()
        if stripped_last_line != "":
            input_paragraphs.append(
                InputParagraph(last_actor_id, stripped_last_line)
            )

    # Build the input text
    return InputText(input_paragraphs)