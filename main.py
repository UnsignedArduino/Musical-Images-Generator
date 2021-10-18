from argparse import ArgumentParser
from pathlib import Path

from mido import MidiFile
from typing import Iterable
from itertools import groupby

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


def chord_to_col(notes: Iterable[int]) -> list[str]:
    column = []
    for row in range(88):
        column.append("f" if row in notes else ".")
    return column


def time_to_col(time: int) -> list[str]:
    # Gets binary representation of time and splits it up and formats it
    # into Arcade-style image values ("1" is white, "." is transparent)
    # >>> ["1" if b == "1" else "." for b in bin(4)[2:]]
    # ['1', '.', '.']
    column = ["1" if b == "1" else "." for b in bin(time)[2:]]
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
