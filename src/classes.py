# -*- coding: utf-8 -*-

# Contains the "Note" class used in our program, that represent a note
# and keeps various attributes assigned to it. It also contains static
# methods to get a random note, or convert a whole list.

import random
import re
from time import sleep

import numpy as np
import simpleaudio as sa


# List of notes and figures
NOTE_NAMES = ['DO', 'RE', 'MI', 'FA', 'SOL', 'LA', 'SI']
NOTE_FIGURES = ['r', 'b', 'n', 'c']


class Note:
    def __init__(self, raw_input):
        self.raw_input = raw_input

        self.parsed_data = self.parse()

        # Name of the note (one of NOTE_NAMES)
        self.name = self.parsed_data[0]
        # Figure of the note (one of NOTE_FIGURES)
        self.figure = self.parsed_data[1]
        # Wether the note has its duration extended with a point
        self.has_point = bool(self.parsed_data[2])
        # The frequency of the note
        self.frequency = self.get_frequency()
        # The duration of the note in seconds
        self.duration = self.get_duration()
        # Wether the note is a pause
        self.is_pause = self.name == "Z"

    @staticmethod
    def create_random_note():
        """ Create a random note. """
        raw_note = random.choice(NOTE_NAMES)
        raw_note += random.choice(NOTE_FIGURES)
        return Note(raw_note)

    @staticmethod
    def to_raw(parsed_notes):
        """ Transform a list of Note instances into a list of raw notes, as in the partition files """
        output = []
        for note in parsed_notes:
            new_note = f'{note.name}{note.figure}'
            new_note += 'p' if note.has_point else ''
            output.append(new_note)
        return output

    def parse(self):
        """
        Parse notes in the partitions, and returns a tuple containing the name,
        the duration and whether it contains a point.
        """
        groups = re.findall("([A-Z]*)(r|b|n|c)(p)?", self.raw_input)
        return groups[0]

    def get_frequency(self):
        """ Assign a frequency for each available notes """
        if self.name == "DO":
            return 264
        elif self.name == "RE":
            return 297
        elif self.name == "MI":
            return 330
        elif self.name == "FA":
            return 352
        elif self.name == "SOL":
            return 396
        elif self.name == "LA":
            return 440
        elif self.name == "SI":
            return 495
        return 0

    def get_duration(self):
        """ Get the duration depending on the figure, and if there is a point """
        duration = 0
        if self.figure == 'r':    # "Ronde"
            duration = 1000
        elif self.figure == 'b':  # "Blanche"
            duration = 500
        elif self.figure == 'n':  # "Noire"
            duration = 250
        elif self.figure == 'c':  # "Croche"
            duration = 125
        # If there is a point, set it to half the duration, otherwise 0
        point_duration = duration / 2 if self.has_point else 0
        # Add the duration and the extended duration (point), and normalize it
        return (duration + point_duration) / 1000

    def play(self):
        """ If there is a frequency, play the note, otherwise it is a pause """
        if self.is_pause:
            # Sleep for the duration of the note when the note is "Z"
            sleep(self.duration)
        else:
            # Get timesteps for each sample, "duration" is note duration in seconds
            sample_rate = 44100
            t = np.linspace(0, self.duration, int(self.duration * sample_rate), False)
            # Generate sine wave tone
            tone = np.sin(self.frequency * t * 6 * np.pi)
            # Normalize to 24−bit range
            tone *= 8388607 / np.max(np.abs(tone))
            # Convert to 32−bit data
            tone = tone.astype(np.int32)

            # Convert from 32−bit to 24−bit by building a new byte buffer,
            # skipping every fourth bit
            # Note: this also works for 2−channel audio
            i = 0
            byte_array = []
            for b in tone.tobytes():
                if i % 4 != 3:
                    byte_array.append(b)
                i += 1

            audio = bytearray(byte_array)
            # Start playback
            play_obj = sa.play_buffer(audio, 1, 3, sample_rate)
            # Wait for playback to finish before exiting
            play_obj.wait_done()
