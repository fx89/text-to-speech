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
# Name: text_to_speech/input_text_with_voice.py
#
# Description:
# Combines paragraphs read from a text file within the input-text directory with
# voice actors loaded from the voices.yaml configuration file and checks that all
# the actors referenced from the input text file are present in the configuration.
#
# ===============================================================================

from text_to_speech.exceptions import InputTextValidationError
from text_to_speech.input_text import read_input_text_file, InputText
from text_to_speech.voices_config import VoicesConfig


# ===============================================================================

class InputTextWithVoice:
    def __init__(self, input_text, voices):
        # Validate and add the paragraphs
        self.paragraphs = []
        for paragraph in input_text.get_paragraphs():
            # Find the voice of the referenced actor
            # or, if not found, raise an exception
            voice = voices.get_voice_by_actor_id(paragraph.actor_id)
            if voice is None:
                raise InputTextValidationError(
                    "Actor " + paragraph.actor_id + " is not configured"
                )

            # Create and add the paragraph
            self.paragraphs.append(
                InputParagraphWithVoice(
                    paragraph.text,
                    paragraph.actor_id,
                    voice.model_path,
                    voice.voice_name,
                    voice.voice_path
                )
            )

    def get_paragraphs(self):
        return self.paragraphs


class InputParagraphWithVoice:
    def __init__(self, text, actor_id, model_path, voice_name, voice_path):
        self.text = text
        self.actor_id = actor_id
        self.model_path = model_path
        self.voice_name = voice_name
        self.voice_path = voice_path
