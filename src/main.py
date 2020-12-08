import re
from time import sleep
import numpy as np
import simpleaudio as sa
class Note:
    def __init__(self, raw_input) -> None:
        self.raw_input = raw_input # SOLcp
        self.parsed_data = self.parse() # ('SOL', 'c', 'p')

        self.frequency = self.get_frequency()
        self.duration = self.get_duration()

    def parse(self):
        groups = re.findall("([A-Z]*)(r|b|n|c)(p)?", self.raw_input)
        return groups[0]

    def get_frequency(self):
        """ Assign a frequency for each available notes """
        if self.parsed_data[0] == "DO":
            return 264
        elif self.parsed_data[0] == "RE":
            return 297
        elif self.parsed_data[0] == "MI":
            return 330
        elif self.parsed_data[0] == "FA":
            return 352
        elif self.parsed_data[0] == "SOL":
            return 396
        elif self.parsed_data[0] == "LA":
            return 440
        elif self.parsed_data[0] == "SI":
            return 495
        else:
            return 0

    def get_duration(self):
        """ Get the duration depending on the figure, and if there is a point """
        has_point = bool(self.parsed_data[2])
        duration = 0
        if self.parsed_data[1] == 'r':
            duration = 1000
        elif self.parsed_data[1] == 'b':
            duration = 500
        elif self.parsed_data[1] == 'n':
            duration = 250
        elif self.parsed_data[1] == 'c':
            duration = 125
        # If there is a point, set it to half the duration, otherwise 0
        point_duration = duration / 2 if has_point else 0
        # Add the duration and the extended duration (point), and normalize it
        return (duration + point_duration) / 1000

    def play(self):
        """ If there is a frequency, play the note, otherwise it is a pause """
        if self.frequency != 0:
            # Get timesteps for each sample, "duration" is note duration in seconds
            sample_rate = 44100
            t = np.linspace(0, self.duration, int(self.duration * sample_rate), False)
            # Generate sine wave tone
            tone = np.sin(self.frequency * t * 6 * np.pi)
            # Normalize to 24−bit range
            tone *= 8388607 / np.max(np.abs(tone))
            # Convert to 32−bit data
            tone = tone.astype(np.int32)

            # Convert from 32−bit to 24−bit by building a new byte buffer ,
            # Skipping every fourth bit
            # Note: this also works for 2−channel audio
            i = 0
            byte_array = [ ]
            for b in tone.tobytes():
                if i % 4 != 3:
                    byte_array.append(b)
                i += 1

            audio = bytearray(byte_array)
            # Start playback
            play_obj = sa.play_buffer(audio, 1, 3, sample_rate)
            # Wait for playback to finish before exiting
            play_obj.wait_done()
        else:
            # Sleep for the duration of the note when the note is "Z"
            sleep(self.duration)


file = open("./assets/partitions.txt", "r")
lines = file.readlines()
file.close()


def get_notes_from_line(line):
    last_char_is_upper = True
    raw_notes_list = []
    current_note = ""

    for char in line:
        if not last_char_is_upper and char.isupper():
            last_char_is_upper = True
            raw_notes_list.append(current_note)
            current_note = char
        else:
            if char.isupper():
                last_char_is_upper = True
            else:
                last_char_is_upper = False
            current_note += char

    return raw_notes_list


# Get the first line, remove the last 2 characters (\n), and remove spaces
curr_line = lines[3][:-1].replace(' ', '')
raw_notes = get_notes_from_line(curr_line)
for raw_note in raw_notes:
    note = Note(raw_note)
    note.play()
