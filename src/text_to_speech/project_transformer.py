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
from text_to_speech.exceptions import ProjectDirectoryValidationError
from text_to_speech.transformer import transform
from text_to_speech.voices_config import VoicesConfig


# ===============================================================================

def transform_project(project_path):
    # Compose paths
    voices_path = os.path.join(project_path, "voices.yaml")
    input_text_path = os.path.join(project_path, "input-text")
    output_audio_path = os.path.join(project_path, "output-audio")

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
    # Create the output directory in case it does not exist
    os.makedirs(output_audio_path, exist_ok=True)

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

    # File names
    file_base_name = os.path.splitext(filename)[0]
    input_file_base_path = os.path.join(root_path, file_base_name)
    output_file_base_path = os.path.join(output_directory, file_base_name)

    # Transform the file
    transform(input_file_base_path, output_file_base_path, voices)
