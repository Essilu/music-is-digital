import turtle as tr
import copy
import random
from classes import Note

# List of notes and figures
NOTE_NAMES = ['DO', 'RE', 'MI', 'FA', 'SOL', 'LA', 'SI']
NOTE_FIGURES = ['r', 'b', 'n', 'c']


def skip_lines(nb):
    print("\n" * (nb-1))


def selector(possibilities, names):
    """ Print a selector of all possibilities, and validate the choice against the "names" list """
    # Print all possibilities
    for i in range(len(possibilities)):
        print(f'({i +1})  {possibilities[i]}')
        names.append(str(i + 1))
    skip_lines(1)
    # Ask a user for a choice
    choice = str(input("Select a category by using its index or by spelling it: "))
    choice = choice.upper()
    # Verify that the choice is possible
    while choice not in names:
        choice = str(input("Select a category by using its index or by spelling it: "))
        choice = choice.upper()
    return choice


def choose_number(maximum):
    """ Chooses an integer between 1 and maximum, always return a valid number """
    while True:
        try:
            skip_lines(1)
            index = int(input(f"Choose a number between 1 and {int(maximum)}: "))
            if index <= 0 or index > maximum:
                raise IndexError
            break
        except ValueError:
            print("Oops! That's not a valid number. Try again...")
        except IndexError:
            print(f"Oops! That number is not possible. It has to be between 1 and {int(maximum)}. Try again...")
    return index


def choose_partition():
    """ Let the user choose a partition amongst the original one and those "home made" """
    # Ask the user wether the partitions should be taken from the original partitions, or from the home-made partitions
    file_name = selector(["The original partition given by the instructor", "The homemade partition file"], ["ORIGINAL", "HOMEMADE"])

    # Open the corresponding file
    if file_name == "1" or file_name == "ORIGINAL":
        file = open("./assets/partitions.txt", "r")
    elif file_name == "2" or file_name == "HOMEMADE":
        file = open("./assets/homemade_partitions.txt", "r")

    skip_lines(30)

    # Print all song's names in the partitions
    lines = file.readlines()
    file.close()
    for i in range(0, len(lines), 2):
        print(lines[i][:-1])

    # Ask the user to choose for a song
    song_index = choose_number(len(lines) / 2)

    # Get the corresponding song's partition and convert notes to Note instances
    partition = lines[song_index * 2 - 1][:-1].replace(' ', '')
    raw_notes = get_notes_from_line(partition)
    parsed_notes = [Note(note) for note in raw_notes]
    return parsed_notes


def save_to_file(content, song_name):
    """ Save a partition to a file """
    file = open("./assets/homemade_partitions.txt", "a+")
    # Move to the start of the file
    file.seek(0)
    # Read the total lines
    total_lines = len(file.readlines())
    # Move to the end of the file
    file.seek(0, 2)
    # Write the song's name
    file.write(f"#{int(total_lines / 2 + 1)} {song_name}\n")
    # Write the song's partition
    file.write(content + "\n")
    file.close()


def music_player(raw_array_to_play, method):
    """ Little menu to play/save/quit when a song has been chosen/created """
    parsed_array_to_play = [Note(note) for note in raw_array_to_play]
    as_string = ' '.join(raw_array_to_play)

    skip_lines(30)

    print(f"Here is your {method} partition:")
    print(as_string)
    skip_lines(1)

    # While the user has not quit the program, show the menu
    while True:
        # Ask the user if they want to Play the song, Save it, or quit the program
        option = selector(["Play", "Save", "Quit"], ["PLAY", "SAVE", "QUIT"])
        if option == "PLAY" or option == "1":
            skip_lines(30)
            print("Playing...")

            tr.bgcolor("black")
            x = 10
            colors = ["red", "purple", "blue", "green", "orange", "yellow"]

            for note in parsed_array_to_play:
                if not note.is_pause:
                    tr.speed('fastest')
                    # The note type change the color
                    tr.color(colors[NOTE_NAMES.index(note.name) % 6])
                    tr.circle(x)
                    tr.up()
                    tr.right(90)
                    # The duration changes the spacing between circles
                    tr.fd(note.duration * 30)
                    tr.left(90)
                    tr.down()
                    x = x + note.duration * 30
                note.play()
            print("End of the song")
            skip_lines(1)

        elif option == "SAVE" or option == "2":
            skip_lines(30)
            print(f"Here is your {method} partition:")
            print(as_string)
            skip_lines(1)
            song_name = input("Insert the name of the song to save: ")
            save_to_file(as_string, song_name)
            print("Partition saved as", song_name, "in homemade_partitions.txt")

        elif option == "QUIT" or option == "3":
            skip_lines(30)
            print("End of program")
            break


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
    raw_output = []
    for note in note_list:
        # We transpose every notes except for Z
        if note.is_pause:
            raw_output.append(f'{note.name}{note.figure}')
        else:
            # Get the index of the note to transpose
            note_name_index = NOTE_NAMES.index(note.name)
            # Get the transposed index according to  the amount
            transposed_index = (note_name_index + amount) % len(NOTE_NAMES)
            new_note_name = NOTE_NAMES[transposed_index]
            # Create the new note, with the new note's name, and its original figure
            new_note = f'{new_note_name}{note.figure}'
            new_note += 'p' if note.has_point else ''
            raw_output.append(new_note)
    return raw_output


def inverse_notes(note_list):
    """ Inverse notes with (total - note_number) % total """
    raw_output = []
    for note in note_list:
        # We transpose every notes except for Z
        if note.is_pause:
            raw_output.append(f'{note.name}{note.figure}')
        else:
            # Get the index of the note to transpose
            note_name_index = NOTE_NAMES.index(note.name)
            # Get the transposed index according to  the amount
            inverted_index = ((len(NOTE_NAMES) - note_name_index) % len(NOTE_NAMES))
            new_note_name = NOTE_NAMES[inverted_index]
            # Create the new note, with the new note's name, and its original figure
            new_note = f'{new_note_name}{note.figure}'
            new_note += 'p' if note.has_point else ''
            raw_output.append(new_note)

    return raw_output


def get_probability_matrix(parsed_note_list):
    """ Get the probability matrix for a given partition """
    # We get the array of note's names, and filter out the Zs
    note_names = [note.name for note in parsed_note_list if not note.is_pause]
    # Create an empty matrix filled with each note (as rows and columns)
    notes_matrix = {name: {name: 0 for name in NOTE_NAMES} for name in NOTE_NAMES}

    # Build the matrix with the given list
    for i in range(len(note_names)):
        index = (i + 1) % len(note_names)
        successor = note_names[index]
        notes_matrix[note_names[i]][successor] += 1
    return notes_matrix


def add_figure(note):
    return f'{note}{random.choice(NOTE_FIGURES)}'


def markov_v1(total, note_list):
    """ Get back a list of notes, chosen with the markov process (without taking occurrences into account) """

    # Step 1: Generate the statistics
    dataset = get_probability_matrix(note_list)
    notes_matrix = copy.deepcopy(dataset)

    # Step 2: Choose a random starting note
    current_note = random.choice(NOTE_NAMES)

    # Step 3: Choose notes among successor
    output = [add_figure(current_note)]
    for _ in range(total):
        non_zero_notes = [note for (note, amount) in notes_matrix[current_note].items() if amount > 0]
        note = random.choice(non_zero_notes)
        output.append(add_figure(note))
        current_note = note

    return output, dataset


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

    # Create the matrix filled with 0s
    result_matrix = {name: {name: 0 for name in NOTE_NAMES} for name in NOTE_NAMES}

    for i in range(1, 24, 2):
        # Remove the \n at the end of the line, and remove spaces
        line = lines[i][:-1].replace(' ', '')
        notes = get_notes_from_line(line)
        notes = [Note(note) for note in notes]
        # Get the probability matrix for the notes
        current_matrix = get_probability_matrix(notes)
        # Add the current line to the top line, to get the total note frequencies
        for note in NOTE_NAMES:
            result_matrix[note] = merge_2_dictionnaries(current_matrix[note], result_matrix[note])

    return result_matrix


def markov_v2(total, parsed_note_list=None, run_from_database=False):
    """ Get back a list of notes, chosen with the markov process (taking occurrences into account) """

    # Step 1: Generate the statistics
    dataset = analyze_db() if run_from_database else get_probability_matrix(parsed_note_list)
    notes_matrix = copy.deepcopy(dataset)

    # Step 2: Choose a starting note which is the most common one
    cumulative_notes_occurences = merge_n_dictionnaries(list(notes_matrix.values()))
    current_note = max(cumulative_notes_occurences)

    # Step 3: Choose notes among successor
    output = [add_figure(current_note)]
    for _ in range(total):
        # Use the choices function with the weight (weights are stored in the keys of the matrix)
        population = list(notes_matrix[current_note].keys())
        weights = list(notes_matrix[current_note].values())

        note = random.choices(population, weights)[0]

        output.append(add_figure(note))
        current_note = note

    return output, dataset
