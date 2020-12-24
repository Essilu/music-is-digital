import json
import classes
from functions import *


print("### Welcome to the project 'Music is Digital', made by Elliot Maisl and Ulysse Juget.")
skip_lines(1)
print("Please, choose what algorithm to use!")

algorithm = selector([
    "Play (normal)",
    "Inverse",
    "Transpose",
    "Markov chains 1 (Without taking into account the number of occurrences of notes)",
    "Markov chains 2 (Taking into account the number of occurrences of notes)"
], ["PLAY", "INVERSE", "TRANSPOSE", "MARKOV CHAINS 1", "MARKOV CHAINS 2"])

skip_lines(30)

if algorithm == "PLAY" or algorithm == "1":
    parsed_notes = choose_partition()
    for note in parsed_notes:
        note.play()

elif algorithm == "INVERSE" or algorithm == "2":
    parsed_notes = choose_partition()

    inverted, raw_inverted = inverse_notes(parsed_notes)
    inverted_as_string = ' '.join(raw_inverted)

    skip_lines(30)

    print("Here is your inverted partition:")
    print(inverted_as_string)

    skip_lines(1)

    while True:
        option = selector(["Play", "Save", "Quit"], ["PLAY", "SAVE", "QUIT"])
        if option == "PLAY" or option == "1":
            skip_lines(30)
            print("Playing...")
            for note in inverted:
                note.play()
            print("End of the song")
            skip_lines(1)
        elif option == "SAVE" or option == "2":
            skip_lines(30)
            song_name = input("Insert the name of the song to save: ")
            save_to_file(inverted_as_string, song_name)
            print("Partition saved as", song_name, "in homemade_partitions.txt")
        elif option == "QUIT" or option == "3":
            skip_lines(30)
            print("End of program")
            break

elif algorithm == "TRANSPOSE" or algorithm == "3":
    parsed_notes = choose_partition()

elif algorithm == "MARKOV CHAINS 1" or algorithm == "4":
    print("You choosed to generate a song with the Markov's algorithm, but without taking into account the number of occurences.")

elif algorithm == "MARKOV CHAINS 2" or algorithm == "5":
    print("You choosed to generate a song with the Markov's algorithm, by into account the number of occurences.")


# file = open("./assets/partitions.txt", "r")
# lines = file.readlines()
# file.close()
#
# music_index = int(input("Enter a music to play (1, 3, 5, 7...)"))
#
# # Extremely temporary, to be replaced by a proper selector thingy.
# # It just allows us to keep our test code, and try different functions easily.
# # test_type has to be one of "normal", "markovv1", "transpose", "inverse", "markovv2"
# test_type = "markovv2-db"
#
# if test_type == "normal" or test_type == "markovv1" or test_type == "markovv2" or test_type == "markovv2-db":
#     # Get the first line, remove the last 2 characters (\n), and remove spaces
#     line = lines[music_index][:-1].replace(' ', '')
#     raw_notes = get_notes_from_line(line)
#     raw_notes = [classes.Note(note) for note in raw_notes]
#
#     if test_type == "normal":
#         for note in raw_notes:
#             note.play()
#     elif test_type == "markovv1":
#         print(markov_v1(raw_notes, 10))
#     elif test_type == "markovv2":
#         print(markov_v2(raw_notes, 20))
#     elif test_type == "markovv2-db":
#         print(markov_v2(raw_notes, 20, True))
#
#         result_matrix = analyze_db()
#         with open('./assets/db_analysis.json', 'w') as fp:
#             json.dump(result_matrix, fp, indent=4)
#
# elif test_type == "transpose" or test_type == "inverse":
#     notes = [Note.create_random_note() for i in range(15)]
#     if test_type == "transpose":
#         print(transpose_notes(notes, 10))
#     elif test_type == "inverse":
#         print(inverse_notes(notes, 10))
#
