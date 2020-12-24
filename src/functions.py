import random
from classes import Note

# List of notes and figures
NOTE_NAMES = ['DO', 'RE', 'MI', 'FA', 'SOL', 'LA', 'SI']
NOTE_FIGURES = ['r', 'b', 'n', 'c']


def skip_lines(nb):
    print("\n" * (nb-1))


def selector(possibilities, names):
    """ Print a selector of all possibilities, and validate the choice against the "names" list """
    for i in range(len(possibilities)):
        print(f'({i +1})  {possibilities[i]}')
        names.append(str(i + 1))
    print("")
    choice = str(input("Select a category by using it's index or by spelling it: "))
    choice = choice.upper()
    print("")
    while choice not in names:
        choice = str(input("Select a category by using it's index or by spelling it: "))
        choice = choice.upper()
    return choice


def choose_index(maximum):
    """ Chooses an integer index in between 1 and maximum, always return a valid index """
    while True:
        try:
            index = int(input("Choose the index of the song you want to play: "))
            if index <= 0 or index > maximum:
                raise IndexError
            break
        except ValueError:
            print("Oops! That's not a valid number. Try again...")
        except IndexError:
            print(f"Oops! That index doesn't exist. It has to be between 1 and {int(maximum)}. Try again...")
    return index


def choose_partition():
    file_name = selector(["The original partition given by the instructor", "The homemade partition file"], ["ORIGINAL", "HOMEMADE"])

    if file_name == "1" or file_name == "ORIGINAL":
        file = open("./assets/partitions.txt", "r")
    elif file_name == "2" or file_name == "HOMEMADE":
        file = open("./assets/homemade_partitions.txt", "r")

    lines = file.readlines()
    file.close()
    for i in range(0, len(lines), 2):
        print(lines[i][:-1])

    song_index = choose_index(len(lines) / 2)

    partition = lines[song_index * 2 - 1][:-1].replace(' ', '')
    raw_notes = get_notes_from_line(partition)
    parsed_notes = [Note(note) for note in raw_notes]
    return parsed_notes


def save_to_file(content, song_name):
    file = open("./assets/homemade_partitions.txt", "r")
    total_lines = len(file.readlines())
    file.close()

    file = open("./assets/homemade_partitions.txt", "a")
    file.write(f"#{int(total_lines / 2 + 1)} {song_name}\n")
    file.write(content + "\n")
    file.close()


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
    parsed_output, raw_output = [], []
    for note in note_list:
        if note.is_pause:
            raw_output.append(f'{note.name}{note.figure}')
            parsed_output.append(note)
        else:
            note_name_index = NOTE_NAMES.index(note.name)
            inverted_index = ((len(NOTE_NAMES) - note_name_index) % len(NOTE_NAMES))
            new_note_name = NOTE_NAMES[inverted_index]
            new_note = f'{new_note_name}{note.figure}'
            new_note += 'p' if note.has_point else ''
            raw_output.append(new_note)
            parsed_output.append(Note(new_note))

    return parsed_output, raw_output


def get_probability_matrix(note_list):
    # We get the array of note's names, and filter out the Zs
    note_names = [note.name for note in note_list if not note.is_pause]
    # Create an empty matrix filled with each note (as rows and columns)
    notes_matrix = {name: {name: 0 for name in NOTE_NAMES} for name in NOTE_NAMES}

    # Build the matrix with the given list
    for i in range(len(note_names)):
        index = (i + 1) % len(note_names)
        successor = note_names[index]
        notes_matrix[note_names[i]][successor] += 1
    return notes_matrix


def markov_v1(note_list, total):
    """ Get back a list of notes, chosen with the markov process (without taking occurrences into account) """

    # Step 1: Generate the statistics
    notes_matrix = get_probability_matrix(note_list)

    # Step 2: Choose a random starting note
    current_note = random.choice(NOTE_NAMES)

    # Step 3: Choose notes among successor
    output = []
    for _ in range(total):
        non_zero_notes = [note for (note, amount) in notes_matrix[current_note].items() if amount > 0]
        note = random.choice(non_zero_notes)
        output.append(note)
        current_note = note

    return output


def merge_2_dictionnaries(dict1, dict2):
    """ Merge two dictionnaries together by adding the values """
    result = dict1
    for k, v in dict2.items():
        result[k] = (result.get(k) or 0) + v
    return result


def merge_n_dictionnaries(dicts):
    """ Merge n dictionnaries together by adding the values """
    result = dicts[0]
    for i in range(1, len(dicts)):
        result = merge_2_dictionnaries(result, dicts[i])
    return result


def analyze_db():
    """ Runs a statistical analysis of the """
    file = open("./assets/partitions.txt", "r")
    lines = file.readlines()
    file.close()

    result_matrix = {name: {name: 0 for name in NOTE_NAMES} for name in NOTE_NAMES}

    for i in range(1, 24, 2):
        line = lines[i][:-1].replace(' ', '')
        print(line)
        notes = get_notes_from_line(line)
        notes = [Note(note) for note in notes]
        current_matrix = get_probability_matrix(notes)
        for note in NOTE_NAMES:
            result_matrix[note] = merge_2_dictionnaries(current_matrix[note], result_matrix[note])

    return result_matrix


def markov_v2(note_list, total, run_from_db=False):
    """ Get back a list of notes, chosen with the markov process (taking occurrences into account) """

    # Step 1: Generate the statistics
    if run_from_db:
        notes_matrix = analyze_db()
    else:
        notes_matrix = get_probability_matrix(note_list)

    # Step 2: Choose a starting note which is the most common one
    cumulative_notes_occurences = merge_n_dictionnaries(list(notes_matrix.values()))
    current_note = max(cumulative_notes_occurences)

    # Step 3: Choose notes among successor
    output = [current_note]
    for _ in range(total):
        # Use the choices function with the weight (weights are stored in the keys of the matrix)
        population = list(notes_matrix[current_note].keys())
        weights = list(notes_matrix[current_note].values())

        note = random.choices(population, weights)[0]

        output.append(note)
        current_note = note

    return output
