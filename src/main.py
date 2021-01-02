# -*- coding: utf-8 -*-

# Program's entry point. It contains the main logic to ask the user what to do.

from classes import Note
from functions import *
from prettytable import PrettyTable


print("Welcome to the project 'Music is Digital', made by Elliot Maisl and Ulysse Juget.")
skip_lines(1)
print("Please, choose what algorithm to use.")
skip_lines(1)

algorithm = selector([
    "Play (normal)",
    "Inverse",
    "Transpose",
    "Markov chains 1 (Without taking into account the number of occurrences of notes)",
    "Markov chains 2 (Taking into account the number of occurrences of notes)"
], ["PLAY", "INVERSE", "TRANSPOSE", "MARKOV CHAINS 1", "MARKOV CHAINS 2"])

skip_lines(30)

if algorithm == "PLAY" or algorithm == "1":
    print("Choose a file to play the music from.")
    skip_lines(1)

    parsed_notes = choose_partition()
    raw_notes = Note.to_raw(parsed_notes)
    music_player(raw_notes, '')

elif algorithm == "INVERSE" or algorithm == "2":
    print("Choose a file to get the music from and invert it.")
    skip_lines(1)

    parsed_notes = choose_partition()
    raw_inverted = inverse_notes(parsed_notes)
    music_player(raw_inverted, "inverted")

elif algorithm == "TRANSPOSE" or algorithm == "3":
    print("Choose a file to get the music from and transpose it.")
    skip_lines(1)

    parsed_notes = choose_partition()
    skip_lines(1)
    print("Choose the amount of the transposition.")
    amount = choose_number(7)

    raw_transposed = transpose_notes(parsed_notes, amount)
    music_player(raw_transposed, "transposed")

elif algorithm == "MARKOV CHAINS 1" or algorithm == "4":
    print("You choosed to generate a song with the Markov's algorithm, but without taking into account the number of occurences.")
    skip_lines(1)
    print("Choose the amount of notes to generate.")

    amount = choose_number(100)
    skip_lines(30)

    parsed_notes = choose_partition()
    skip_lines(30)
    raw_notes, dataset = markov_v1(amount, parsed_notes)

    # Create a table with an external library
    table = PrettyTable()
    notes_names = ['DO', 'RE', 'MI', 'FA', 'SOL', 'LA', 'SI']
    # Add headers
    table.field_names = ['X', *notes_names]
    # Add rows
    for note in notes_names:
        table.add_row([note, *dataset[note].values()])
    print(table)
    skip_lines(1)

    music_player(raw_notes, "Markov Chains 1", False)

elif algorithm == "MARKOV CHAINS 2" or algorithm == "5":
    print("You choosed to generate a song with the Markov's algorithm, by into account the number of occurences.")
    print("Choose from where to generate all the data.")
    skip_lines(1)
    source = selector(["Whole partition database", "A specific partition"], ["DATABASE", "PARTITION", "SPECIFIC"])

    skip_lines(30)

    print("Choose the amount of notes to generate.")
    amount = choose_number(100)
    skip_lines(30)
    if source in ["DATABASE", "1"]:
        raw_notes, dataset = markov_v2(amount, run_from_database=True)

    elif source in ["PARTITION", "SPECIFIC", "2"]:
        parsed_notes = choose_partition()
        skip_lines(30)
        raw_notes, dataset = markov_v2(amount, parsed_note_list=parsed_notes)

    # Create a table with an external library
    table = PrettyTable()
    notes_names = ['DO', 'RE', 'MI', 'FA', 'SOL', 'LA', 'SI']
    # Add headers
    table.field_names = ['X', *notes_names]
    # Add rows
    for note in notes_names:
        table.add_row([note, *dataset[note].values()])
    print(table)
    skip_lines(1)

    music_player(raw_notes, "Markov Chains 2", False)
