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
# Name: text_to_speech/voices.py
#
# Description:
# Deserializes and validates voices configuration
#
# ===============================================================================

import yaml
import sys

from collections import defaultdict

# ===============================================================================

"""
Entity that defines the model to be loaded and the name to reference in order to
produce a given voice
"""
class Voice:
    def __init__(self, model_path, voice_name):
        self.model_path = model_path
        self.voice_name = voice_name

# ===============================================================================

"""

"""
class Voices:
    def __init__(self, path_to_voices_yaml):
        # Load the voices configuration
        voices_config = load_voices_config(path_to_voices_yaml)

        # Map voices by name
        self.voices_by_name = map_voices_by_name(voices_config)

    def get_voice(self, voice_name):
        return self.voices_by_name[voice_name]

# ===============================================================================

"""
Loops through the voice configuration and creates new Voice entities mapped by
voice name
"""
def map_voices_by_name(voices_config):
    # Create the dictionary
    voices_by_name = defaultdict(dict)

    # Fill the dictionary


    voices_by_name["name"] = Voice("da", "mda")

    # Return the dictionary
    return voices_by_name



"""
Applies verification rules to the loaded voices configuration
"""
def verify_voices_config(voices_config):
    sys.stdout.write(voices_config.models[0])



"""
Loads and verifies the voices configuration
"""
def load_voices_config(path_to_voices_yaml):
    # Load the voices config
    with open(path_to_voices_yaml, 'r') as voices_yaml_file:
        voices_config = yaml.safe_load(voices_yaml_file)

    # Verify the voices config
    verify_voices_config(voices_config)

    # Return voices config
    return voices_config