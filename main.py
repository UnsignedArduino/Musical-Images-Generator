from argparse import ArgumentParser
from pathlib import Path
from math import ceil
from typing import Iterable

from mido import MidiFile

parser = ArgumentParser(description="Turn a MIDI file into MakeCode Arcade "
                                    "images compatible with the "
                                    "Musical-Images extension")
parser.add_argument("path", type=Path,
                    help="The path to the MIDI file")
parser.add_argument("--output_path", type=Path,
                    default=None, help="The path to write the images to")
parser.add_argument("--stdout", action="store_const",
                    const=True, default=False,
                    help="Whether to output everything to standard output "
                         "instead of writing to a file")
args = parser.parse_args()

in_path = args.path.expanduser().resolve()
out_path = args.output_path
to_stdout = args.stdout
if out_path is None:
    # Put output file in the same directory as input file with same name
    # but with different extension
    out_path = in_path.parent / (in_path.stem + ".txt")


def note_num_to_name(num: int) -> str:
    # https://stackoverflow.com/a/54546263/10291933
    notes = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
    octave = ceil(num / 12)
    name = notes[num % 12]
    return name + str(octave)


def chord_to_col(notes: Iterable[int]) -> list[str]:
    column = []
    for row in range(88):
        if "#" in note_num_to_name(row):
            column.append("f" if row in notes else ".")
        else:
            column.append("1" if row in notes else ".")
    return column


def time_to_col(time: int) -> list[str]:
    # Generates every color in Arcade palette except transparent, white and
    # black
    colors = [str(hex(c)[2:]) for c in range(2, 15)]
    times = range(50, 14 * 50, 50)
    # Gets the color to to indicate the time, so red is less then 50 ms,
    # pink is less then 100 ms, orange is less then 150 ms, etc
    # Brown is over 600 ms
    color = colors[-1]
    for c, t in zip(colors, times):
        if time < t:
            color = c
            break
    column = []
    # Gets binary representation of time and splits it up and formats it
    # into Arcade-style image values ("1" is white, "." is transparent)
    for bit in bin(time)[2:]:
        column.append(color if bit == "1" else ".")
    column.reverse()
    column += "." * (88 - len(column))
    return column


mid = MidiFile(in_path)

columns = []
notes_to_press = []

for msg in mid:
    if msg.type != "note_on":
        continue
    if msg.velocity > 0:
        notes_to_press.append(msg.note - 21)
    elif msg.time > 0:
        columns.append(chord_to_col(notes_to_press))
        # The times are in seconds but we need milliseconds
        columns.append(time_to_col(round(msg.time * 1000)))
        notes_to_press = []

output = ""


def chunk(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


# Split all columns into lists of 512 columns (512 is max Arcade image width)
all_columns = chunk(columns, 512)
count = 0

for columns in all_columns:
    count += 1
    output += "img`\n"
    rows = zip(*columns)
    for row in rows:
        output += " ".join(row) + "\n"
    output += "`\n\n"

if to_stdout:
    print(output)
else:
    print(f"Generated {count} image(s)")
    out_path.write_text(output)
    print(f"Output destination file is {out_path}")
