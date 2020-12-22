import json
import classes
from functions import *

file = open("./assets/partitions.txt", "r")
lines = file.readlines()
file.close()


music_index = int(input("Enter a music to play (1, 3, 5, 7...)"))

# Extremely temporary, to be replaced by a proper selector thingy.
# It just allows us to keep our test code, and try different functions easily.
# test_type has to be one of "normal", "markovv1", "transpose", "inverse", "markovv2"
test_type = "markovv2-db"

if test_type == "normal" or test_type == "markovv1" or test_type == "markovv2" or test_type == "markovv2-db":
    # Get the first line, remove the last 2 characters (\n), and remove spaces
    line = lines[music_index][:-1].replace(' ', '')
    raw_notes = get_notes_from_line(line)
    raw_notes = [classes.Note(note) for note in raw_notes]

    if test_type == "normal":
        for note in raw_notes:
            note.play()
    elif test_type == "markovv1":
        print(markov_v1(raw_notes, 10))
    elif test_type == "markovv2":
        print(markov_v2(raw_notes, 20))
    elif test_type == "markovv2-db":
        print(markov_v2(raw_notes, 20, True))

        result_matrix = analyze_db()
        with open('./assets/db_analysis.json', 'w') as fp:
            json.dump(result_matrix, fp, indent=4)

elif test_type == "transpose" or test_type == "inverse":
    notes = [Note.create_random_note() for i in range(15)]
    if test_type == "transpose":
        print(transpose_notes(notes, 10))
    elif test_type == "inverse":
        print(inverse_notes(notes, 10))
