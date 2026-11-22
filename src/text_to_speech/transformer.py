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
# Name: text_to_speech/transformer.py
#
# Description:
# Transforms the text inside a given input file into speech saved into the given
# target file
#
# References:
#    - PTTS: https://github.com/gradium-ai/xn-ptts
#    - PyDub: https://github.com/jiaaro/pydub/
#    - Phonon 31M: https://huggingface.co/gradium/phonon-31m-en/tree/main
#
# ===============================================================================

import ptts
import sys
from pydub import AudioSegment
from text_to_speech.input_text import read_input_text_file, InputText
from text_to_speech.input_text_with_voice import InputTextWithVoice
from text_to_speech.progress_bar import ProgressBar

# ===============================================================================

initial_silence_duration_ms = 100
in_between_silence_duration_ms = 200
progress_bar_prefix = ""


# ===============================================================================

def transform(
        input_text_file_partial_path,
        output_wave_file_partial_path,
        voices
):
    # Compose the input and output file path and name
    input_file_path_name = input_text_file_partial_path + ".txt"
    output_file_path_name = output_wave_file_partial_path + ".wav"

    # Report the input file path and name
    sys.stdout.write("Transforming " + input_file_path_name + "\r\n")

    # Read the input text file
    input_text = read_input_text_file(input_file_path_name)

    # Combine the input text file with the voices configuration
    input_text_with_voice = InputTextWithVoice(input_text, voices)

    # Transform the paragraphs into wave outputs while remembering the file
    # segment paths, which are needed later for putting together the final
    # wave file
    wave_file_segment_paths = []
    paragraphs = input_text_with_voice.get_paragraphs()
    for paragraph_index in ProgressBar(len(paragraphs), progress_bar_prefix):
        # Get the paragraph
        paragraph = paragraphs[paragraph_index]

        # Generate the file name
        wave_file_segment_path = (
                output_wave_file_partial_path +
                "--P" + str(paragraph_index).rjust(5, "0") +
                "-" + paragraph.actor_id.replace(" ", "_") +
                ".wav"
        )

        # Transform using PTTS...

        # Create the TTS transformer
        tts = initialize_tts(paragraph.model_path)

        # Optionally add the custom voice
        voice_name = initialize_voice(tts, paragraph)

        # Transform
        tts.save(wave_file_segment_path, paragraph.text, voice=voice_name)

        # Add the wave segment path to the array
        wave_file_segment_paths.append(wave_file_segment_path)

    # Report the generated files
    sys.stdout.write("Files generated: \r\n")
    for wave_file_segment_path in wave_file_segment_paths:
        sys.stdout.write(" - " + wave_file_segment_path + "\r\n")

    # Stitch the wave file together...
    sys.stdout.write("Combining wave files... \r\n")

    # Initialize the output file
    output_wave_file = AudioSegment.silent(duration=initial_silence_duration_ms)

    # Generate some silence
    silence = AudioSegment.silent(duration=in_between_silence_duration_ms)

    # Loop through the segments
    for wave_file_segment_path in wave_file_segment_paths:
        # Read the wave file
        wave_file = AudioSegment.from_wav(wave_file_segment_path)

        # Append the wave file to the output file
        output_wave_file = output_wave_file + wave_file

        # Append silence between paragraphs
        output_wave_file = output_wave_file + silence

    # Save the output file
    output_wave_file.export(
        output_file_path_name,
        format="wav"
    )

    # Report success
    sys.stdout.write(" - exported " + output_file_path_name + "\r\n")


def initialize_tts(model_path):
    if model_path == "default":
        return ptts.TTS(lang="en")
    else:
        return ptts.TTS(model_path, lang="en")


def initialize_voice(tts, paragraph):
    if paragraph.voice_path is not None:
        voice_name = "custom_dfh23ufdh239f_voice"
        tts.add_voice(voice_name, paragraph.voice_path)
    else:
        voice_name = paragraph.voice_name

    return voice_name
