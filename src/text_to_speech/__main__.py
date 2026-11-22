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
from text_to_speech.project_transformer import transform_project
from text_to_speech.ptts_metadata import list_voices, list_catalog_voices


# ===============================================================================


def main():
    try:
        # Nothing to do if no parameters are provided
        if len(sys.argv) < 2:
            print_usage()
            sys.exit(1)

        # Process the list catalog voices command
        if sys.argv[1] == "list-catalog-voices":
            list_catalog_voices()

        # Process the list-voices command
        elif sys.argv[1] == "list-voices":
            # Model path parameter is mandatory
            if len(sys.argv) < 3:
                list_voices("default")
            else:
                list_voices(sys.argv[2])

        # Process the transform command
        elif sys.argv[1] == "transform":
            # The project path parameter is mandatory
            if len(sys.argv) < 3:
                sys.stderr.write("Syntax error: <path-to-project-dir> not provided\r\n")
                sys.stderr.write("\r\n")
                print_usage()
                sys.exit(1)

            # If the project path parameter has been given,
            # then go ahead and transform
            transform_project(sys.argv[2])

        # If no command was provided, or if the provided command is unknown,
        # then prompt the user and exit
        else:
            sys.stderr.write("Syntax error: unknown command\r\n")
            sys.stderr.write("\r\n")
            print_usage()
            sys.exit(1)

    except Exception as e:
        sys.stderr.write("\r\nError: " + str(e) + "\r\n")
    except KeyboardInterrupt:
        sys.stdout.write("\r\nInterrupted by user. \r\n")


def print_usage():
    sys.stderr.write("Usage: " + sys.argv[0] + " <command> [parameters]\r\n")
    sys.stderr.write("   <command> [parameters] can be either: \r\n")
    sys.stderr.write("      list-catgalog-voices\r\n")
    sys.stderr.write("      list-voices [path-to-model-dir|default]\r\n")
    sys.stderr.write("      transform <path-to-project-dir>\r\n")
    sys.stderr.write("Examples: \r\n")
    sys.stderr.write("   " + sys.argv[0] + "list-catalog-voices\r\n")
    sys.stderr.write("   " + sys.argv[0] + "list-voices /path/to/model\r\n")
    sys.stderr.write("   " + sys.argv[0] + "transform /path/to/project/dir\r\n")


if __name__ == "__main__":
    main()
