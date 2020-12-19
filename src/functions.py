import random
from classes import Note

# List of notes and figures
NOTE_NAMES = ['DO', 'RE', 'MI', 'FA', 'SOL', 'LA', 'SI']
NOTE_FIGURES = ['r', 'b', 'n', 'c']


def get_notes_from_line(line):
    """
    Takes a line as a string, and gives back an array of note symbols (string, with name + figure).

    We didn't just split at each spaces, because we wanted the "p" to be part of
    the note it succeeds, to increase directly the duration of the note.
    Hence, we split the string each time we encounter an uppercase character, preceded
    with a lowercase character, meaning we found the beginning of a new note.
    """
    last_char_is_upper = True
    raw_notes_list = []
    current_note = ""

    for char in line:
        if not last_char_is_upper and char.isupper():
            raw_notes_list.append(current_note)
            current_note = ""

        current_note += char
        last_char_is_upper = char.isupper()

    raw_notes_list.append(current_note)
    return raw_notes_list


def transpose_notes(note_list, amount):
    """ Transpose the note from one to another with an amount x """
    output = []
    for note in note_list:
        # We transpose every notes except for Z
        if note.is_pause:
            output.append(note)
        else:
            # Get the index of the note to transpose
            note_name_index = NOTE_NAMES.index(note.name)
            # Get the transposed index according to  the amount
            transposed_index = (note_name_index + amount) % len(NOTE_NAMES)
            new_note_name = NOTE_NAMES[transposed_index]
            # Create the new note, with the new note's name, and its original figure
            new_note = f'{new_note_name}{note.figure}'
            output.append(Note(new_note))

    return output


def inverse_notes(note_list):
    """ Inverse notes with (total - note_number) % total """
    output = []
    for note in note_list:
        if note.is_pause:
            output.append(note)
        else:
            note_name_index = NOTE_NAMES.index(note.name)
            inverted_index = ((len(NOTE_NAMES) - note_name_index) % len(NOTE_NAMES))
            new_note_name = NOTE_NAMES[inverted_index]
            new_note = f'{new_note_name}{note.figure}'
            output.append(Note(new_note))

    return output


def markov_v1(note_list, total):
    """ Get back a list of notes, chosen with the markov process (without taking occurrences into account) """

    # Step 1: Generate the statistics
    # We get the array of note's names, and filter out the Zs
    note_names = [note.name for note in note_list if not note.is_pause]
    # Create an empty matrix filled with each note (as rows and columns)
    notes_matrix = {name: {name: 0 for name in NOTE_NAMES} for name in NOTE_NAMES}

    # Build the matrix with the given list
    for i, note_name in enumerate(note_names):
        # FIXME: Don't ignore the last note
        if i + 1 == len(note_names):
            continue
        successor = note_names[i + 1]
        notes_matrix[note_name][successor] += 1

    # Step 2: Choose a random starting note
    current_note = random.choice(NOTE_NAMES)

    # Step 3: Choose notes among successor
    output = []
    for i in range(total):
        non_zero_notes = [note for (note, amount) in notes_matrix[current_note].items() if amount > 0]
        note = random.choice(non_zero_notes)
        output.append(note)
        current_note = note

    return output
