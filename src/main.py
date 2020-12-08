import classes
import functions

file = open("./assets/partitions.txt", "r")
lines = file.readlines()
file.close()


music_index = int(input("Enter a music to play (1, 3, 5, 7...)"))

# Get the first line, remove the last 2 characters (\n), and remove spaces
curr_line = lines[music_index][:-1].replace(' ', '')
raw_notes = functions.get_notes_from_line(curr_line)

for raw_note in raw_notes:
    note = classes.Note(raw_note)
    note.play()
