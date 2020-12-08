def get_notes_from_line(line):
    """
    Takes a line as a string, and gives back an array of note.

    We didn't just splitted at each spaces because we wanted the "p" to be part of
    the note it succeeds, to increase directly the duration of the note.
    Hence, we split the string each time we encounter an uppercase character, preceeded
    with a lowercase character, meaning we found the beggining of a new note.
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
