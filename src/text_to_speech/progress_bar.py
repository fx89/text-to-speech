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
# Name: text_to_speech/progress_bar.py
#
# Description:
# Displays a progress bar into stdout
#
# ===============================================================================

import sys
import time


# ===============================================================================

def format_duration(duration):
    int_duration = int(duration)
    nbr_minutes = int(int_duration / 60)
    nbr_seconds = int_duration - (nbr_minutes * 60)

    if nbr_minutes == 0:
        return str(nbr_seconds) + "s"
    else:
        return str(nbr_minutes) + "m " + str(nbr_seconds) + "s"


class ProgressBar:
    """
    Proprietary implementation of a progress bar drawn from unicode characters.

    Looks like this:
    Progress: 【⏺⏺⏺⏺⏺⏺⏺⏺⏺⏺⏺⏺⏺⏺⏺⏺⏺⏺⏺⏺⏺⏺⏺⏺⏺⏺】 100.00%   Time: 12m 34s

    Could use some work
        - code can be shortened using more modern patterns.
        - configuration can be externalized.

    Loads of better implementations exist on the internet, but this is proprietary,
    meaning it can be distributed without issue.
    """

    def __init__(self, top, prefix):
        self.top = top
        self.current = 0
        self.pb_length = 40
        self.pb_char_empty = " "
        # self.pb_char_filled = "█"
        # self.pb_char_filled = "≣"
        # self.pb_char_filled = "⏹"
        self.pb_char_filled = "⏺"
        # self.pb_char_filled = "═"
        self.start_time = time.time()
        self.prefix = prefix

    def __iter__(self):
        return self

    def __next__(self):
        if self.current < self.top:
            self.print_progressbar()
            ret = self.current
            self.current = self.current + 1
            return ret
        else:
            self.print_progressbar()
            print("")
            raise StopIteration

    def print_progressbar(self):
        # Compute the index of the character until which the progres bar is filled
        # Also compute the filled percentage
        if self.current == 0:
            filled_max = 0
            filled_pct = 0
        else:
            filled_max = self.current * self.pb_length / self.top
            filled_pct = self.current * 100 / self.top

        # Compute the progress bar interior
        str_progress = ""
        for i in range(self.pb_length):
            if i <= filled_max:
                str_progress = str_progress + self.pb_char_filled
            else:
                str_progress = str_progress + self.pb_char_empty

        # Compute the elapsed time
        elapsed_time = time.time() - self.start_time

        # Print the entire progress bar
        sys.stdout.write(
            "\r" +
            self.prefix + " 【" + str_progress + " 】" +
            "{:.2f}%".format(filled_pct).rjust(7, " ") +
            "   "
            "Time: " + format_duration(elapsed_time)
        )
        sys.stdout.flush()
