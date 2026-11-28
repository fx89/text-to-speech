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
# Name: text_to_speech/project_transformer.py
#
# Description:
# Applies the transformer on the given project directory, provided that the given
# project directory exists and has a valid structure
#
# ===============================================================================

import os
import sys
import shutil
from text_to_speech.exceptions import ProjectDirectoryValidationError
from text_to_speech.transformer import transform
from text_to_speech.voices_config import VoicesConfig, get_example_voice_file_lines


# ===============================================================================

class ProjectDir:
    def __init__(self, project_path):
        self.voices_path = os.path.join(project_path, "voices.yaml")
        self.input_text_path = os.path.join(project_path, "input-text")
        self.output_audio_path = os.path.join(project_path, "output-audio")
        self.voices_directory_path = os.path.join(project_path, "voices")

# ===============================================================================

def new_project(project_path):
    # Make sure the project path doesn't already exist
    if os.path.isdir(project_path) or os.path.isfile(project_path):
        raise ProjectDirectoryValidationError(
            "The path [" + project_path + "] cannot be created " +
            "because it already exists."
        )

    # Create the project directory
    os.makedirs(project_path, exist_ok=False)

    # Compose the project paths
    project_dir = ProjectDir(project_path)

    # Create the input-text directory
    os.makedirs(project_dir.input_text_path, exist_ok=False)

    # Create the voices directory
    os.makedirs(project_dir.voices_directory_path, exist_ok=False)

    # Create the output-audio directory
    os.makedirs(project_dir.output_audio_path, exist_ok=False)

    # Create the voices.yaml config file
    with open(project_dir.voices_path, "w") as f:
        f.writelines(get_example_voice_file_lines())

    # Create the sample input file
    sample_input_file_path = os.path.join(project_dir.input_text_path, "0000-0000-example.txt")
    with open(sample_input_file_path, "w") as f:
        f.writelines([
            "{{NARRATOR}} This is a sample line\r\n",
            "\r\n",
            "{{MAIN_CHARACTER}}\r\n",
            "This is another sample line\r\n",
            "\r\n",
            "{{NARRATOR}} For a comprehensive example, visit the example project at {{MAIN_CHARACTER}} https://github.com/fx89/text-to-speech/tree/main/example-project\r\n"
        ])

    # Report success
    sys.stdout.write("New project created in [" + project_path + "]\r\n")


# ===============================================================================

def transform_project(project_path):
    # Compose paths
    project_dir = ProjectDir(project_path)
    voices_path = project_dir.voices_path
    input_text_path = project_dir.input_text_path
    output_audio_path = project_dir.output_audio_path

    # Validate the project directory
    validate_project_directory(project_path, voices_path, input_text_path)

    # Read the voices configuration
    voices = VoicesConfig(project_path, voices_path)

    # Transform the input-text files in the project directory
    # using the voices configuration loaded above
    transform_project_directory(
        input_text_path,
        output_audio_path,
        voices
    )


def validate_project_directory(
        project_path,
        voices_path,
        input_text_path
):
    # Make sure the project path exists
    if not os.path.exists(project_path):
        raise ProjectDirectoryValidationError(
            "The path [" + project_path + "] does not exist."
        )

    # Make sure the voices.yaml file exists
    if not os.path.exists(voices_path):
        raise ProjectDirectoryValidationError(
            "The path [" + voices_path + "] does not exist."
        )

    # Make sure the input-text path exists
    if not os.path.exists(input_text_path):
        raise ProjectDirectoryValidationError(
            "The path [" + input_text_path + "] does not exist."
        )


def transform_project_directory(
        input_text_path,
        output_audio_path,
        voices
):
    # Delete the output directory in case it already exists (to clean it up)
    if os.path.exists(output_audio_path):
        shutil.rmtree(output_audio_path)

    # Create the output directory
    os.makedirs(output_audio_path, exist_ok=False)

    # Walk the input text path recursively
    for root, dirs, files in os.walk(input_text_path):
        for filename in files:
            # Skip any file that does not have the .txt extension
            if os.path.splitext(filename)[1] != ".txt":
                continue

            # Transform the file
            transform_file(
                root,
                filename,
                input_text_path,
                output_audio_path,
                voices
            )

            # Next
            sys.stdout.write("\r\n")


def transform_file(
        root_path,
        filename,
        input_text_path,
        output_audio_path,
        voices
):
    # Directories
    output_directory = root_path.replace(input_text_path, output_audio_path)

    # Make sure the output directory exists
    os.makedirs(output_directory, exist_ok=True)

    # File names
    file_base_name = os.path.splitext(filename)[0]
    input_file_base_path = os.path.join(root_path, file_base_name)
    output_file_base_path = os.path.join(output_directory, file_base_name)

    # Transform the file
    transform(input_file_base_path, output_file_base_path, voices)
