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
# Name: text_to_speech/voices_config.py
#
# Description:
# Deserializes and validates voices configuration
#
# ===============================================================================

import os
import yaml
from collections import defaultdict
from text_to_speech.exceptions import ConfigurationError


# ===============================================================================

def get_example_voice_file_lines():
    return [
        "# Maps models to short IDs for easier reference in the voices section\r\n",
        "models:\r\n",
        "  - model_id: phonon-31m-en # User-defined ID\r\n",
        "    model_path: /path/to/phonon/model # Path to the model (either relative (to the project directory) or absolute local directory or hugging faces URL [hf://owner/name@revision])\r\n"
        "\r\n",
        "# Defines the voice actors to be used in the script and maps them to model voices\r\n",
        "# To define this, one must be aware of the list of available voices for each model\r\n",
        "# This can be done by calling text-to-speech.py with the \"--list-voices\" flag\r\n",
        "# More information in the readme\r\n",
        "actors:\r\n",
        "  - actor_id: NARRATOR # This can be used in text files under the \"input-text\" directory to identify the voice to speak a given paragraph\r\n",
        "#   model_id: phonon-31m-en # Reference to the models section\r\n",
        "    model_id: default\r\n",
        "    voice_name: Hugh # Name of the voice - to list voices, run text-to-speech.py [-m <model-path>] --list-voices\r\n",
        "\r\n",
        "  - actor_id: MAIN_CHARACTER\r\n",
        "    model_id: default\r\n",
        "    voice_name: Annika\r\n",
        "\r\n",
        "    # The voice name may be replaced by the path to a custom voice\r\n"
        "  - actor_id: MR_DEFAULT\r\n",
        "    model_id: default\r\n",
        "    voice_path: voices/optional-phonon-31m-default-voice.safetensors # The path can be either absolute or relative to the project directory\r\n"
    ]

# ===============================================================================

class VoiceConfig:
    """
    Entity that defines the model to be loaded and the name to reference in order to
    produce a given voice
    """

    def __init__(self, model_path, voice_name, voice_path):
        self.model_path = model_path
        self.voice_name = voice_name
        self.voice_path = voice_path


# ===============================================================================

class VoicesConfig:
    """
    Loader for the voices configuration file
    """

    def __init__(
            self,
            project_path,
            path_to_voices_yaml
    ):
        # Load the voices configuration
        voices_config = load_voices_config(path_to_voices_yaml)

        # Map voices by name
        self.voices_by_actor_id = map_voices_by_actor_id(
            project_path,
            voices_config
        )

    def get_voice_by_actor_id(self, actor_id):
        if actor_id in self.voices_by_actor_id:
            return self.voices_by_actor_id[actor_id]
        else:
            return None


# ===============================================================================

def map_voices_by_actor_id(
        project_path,
        voices_config
):
    """
    Loops through the voice configuration and creates new Voice entities mapped by
    voice id
    """
    # Create a dictionary of model paths by model id
    model_paths_by_model_id = defaultdict(list)

    # If the voices config file has models, then populate the dictionary
    if "models" in voices_config:
        models = voices_config["models"]
        if models is not None:
            for model in voices_config["models"]:
                model_id = validate_model_entry(model)
                model_path = model["model_path"]

                # If the model path is not absolute, then make it
                # relative to the project directory, unless it's a
                # Hugging Faces path, in which case just leave it
                # like it is
                if not os.path.isabs(model_path):
                    if not model_path.startswith("hf://"):
                        model_path = os.path.join(project_path, model_path)

                model_paths_by_model_id[model_id] = model_path

    # Create the dictionary
    voices_by_actor_id = defaultdict(dict)

    # Fill the dictionary
    for actor in voices_config["actors"]:
        actor_id = validate_actor_entry(actor)

        # Get the model id declared in the voice
        model_id = actor["model_id"]

        # If it's the default model, then just set it to default
        if model_id == "default":
            model_path = "default"
        else:
            # If it's not the default model, then look up the model referenced
            # by the voice
            if model_id not in model_paths_by_model_id:
                raise ConfigurationError("Model " + model_id + " not defined in"
                                                               " voices config")
            model_path = model_paths_by_model_id[model_id]

        # Get the voice name, if any
        if "voice_name" in actor:
            voice_name = actor["voice_name"]
        else:
            voice_name = None

        # Get the voice voice_path, if any
        if "voice_path" in actor:
            voice_path = actor["voice_path"]

            # If the voice path is not absolute, then make it
            # relative to the project directory
            if not os.path.isabs(voice_path):
                voice_path = os.path.join(project_path, voice_path)
        else:
            voice_path = None

        # Add the voice to the dictionary
        voices_by_actor_id[actor_id] = VoiceConfig(
            model_path, voice_name, voice_path
        )

    # Return the dictionary
    return voices_by_actor_id


def load_voices_config(path_to_voices_yaml):
    """
    Loads and verifies the voices configuration
    """
    # Load the voices config
    with open(path_to_voices_yaml, 'r') as voices_yaml_file:
        voices_config = yaml.safe_load(voices_yaml_file)

    # Return voices config
    return voices_config


def validate_model_entry(model):
    """
    Validates the referenced model entry and returns the model id
    """
    if "model_id" not in model:
        raise ConfigurationError("model_id attribute missing from model")

    model_id = model["model_id"]

    if "model_path" not in model:
        raise ConfigurationError(
            "model_path attribute missing from model " + model_id
        )

    return model_id


def validate_actor_entry(actor):
    """
    Validates the referenced actor entry and returns the actor id
    """
    if "actor_id" not in actor:
        raise ConfigurationError("actor_id attribute missing from actor")

    actor_id = actor["actor_id"]

    if "model_id" not in actor:
        raise ConfigurationError(
            "model_id attribute missing from actor " + actor_id
        )

    if "voice_name" not in actor and "voice_path" not in actor:
        raise ConfigurationError(
            "voice_name or voice_path attribute missing from actor " + actor_id
        )

    return actor_id
