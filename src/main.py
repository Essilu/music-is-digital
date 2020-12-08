import re

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
        point_duration = duration / 2 if has_point else 0
        return duration + point_duration


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
curr_line = lines[1][:-1].replace(' ', '')
raw_notes = get_notes_from_line(curr_line)
