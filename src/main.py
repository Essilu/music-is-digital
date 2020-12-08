from note import Note


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
