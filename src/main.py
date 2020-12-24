import json
import classes
from functions import *

#Functions useful in the main program
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


print("### Welcome to the project 'Music is Digital', made by Elliot Maisl and Ulysse Juget.")
print("Please, choose what algorithm to use!")

algorithm = selector([
    "Play (normal)",
    "Inverse",
    "Transpose",
    "Markov chains 1 (Without taking into account the number of occurrences of notes)",
    "Markov chains 2 (Taking into account the number of occurrences of notes)"
], ["PLAY", "INVERSE", "TRANSPOSE", "MARKOV CHAINS 1", "MARKOV CHAINS 2"])

skip_lines(30)

# TODO: Make it impossible to choose impossible algos
if algorithm == "PLAY" or algorithm == "1":
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
    raw_notes = [classes.Note(note) for note in raw_notes]
    for note in raw_notes:
        note.play()

elif algorithm == "INVERSE" or algorithm == "2":
    print("You choosed to play a song with inverted notes.")
    print("(1)  The original partition given by the instructor")
    print("(2)  The homemade partition file")

    file_name = input("Select a category by using it's index or by spelling it: ")

elif algorithm == "TRANSPOSE" or algorithm == "3":
    print("You choosed to play a song with transposed notes.")

    print("(1)  The original partition given by the instructor")
    print("(2)  The homemade partition file")

    file_name = input("Select a category by using it's index or by spelling it: ")

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
