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
# Name: text_to_speech/__main__.py
#
# Description:
# PTTS wrapper script that generates dialogues using multiple voices and models,
# optionally stitching the generated sounds together using Pydub
#
# References:
#    - PTTS: https://github.com/gradium-ai/xn-ptts
#    - PyDub: https://github.com/jiaaro/pydub/
#    - Phonon 31M: https://huggingface.co/gradium/phonon-31m-en/tree/main
#
# ===============================================================================

import sys

import ptts
#from pydub import AudioSegment

from text_to_speech import voices

# from text_to_speech import feed, viewer

def main():
    sys.stderr.write("starting\n")
    tts = ptts.TTS(lang="en")
    tts.save("speech.wav", "Hello from Phonon.")
    sys.stderr.write("ending\n")

if __name__ == "__main__":
    main()