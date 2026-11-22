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
# Name: text_to_speech/ptts_metadata.py
#
# Description:
# Wraps around PTTS functionality for extracting metadata
#
# References:
#    - PTTS: https://github.com/gradium-ai/xn-ptts
#
# ===============================================================================

import os
import ptts
import sys


# ===============================================================================

def list_voices(model_path):
    # Initialize the TTS transformer
    if model_path == "default":
        tts = ptts.TTS(lang="en")
    else:
        tts = ptts.TTS(lang="en", config=model_path)

    # Get and output the voices
    print(tts.voices)


def list_catalog_voices():
    print(ptts.catalog_voices())
