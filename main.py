from argparse import ArgumentParser
from pathlib import Path

parser = ArgumentParser(description="Turn a MIDI file into MakeCode Arcade "
                                    "images compatible with the "
                                    "Musical-Images extension")
parser.add_argument("path", type=Path,
                    help="The path to the MIDI file")
parser.add_argument("--output_path", type=Path,
                    default=None, help="The path to write the images to")
args = parser.parse_args()
in_path = args.path.expanduser().resolve()
out_path = args.output_path
if out_path is None:
    out_path = in_path.parent / (in_path.stem + ".txt")

print(f"Path to MIDI file is {in_path}")



print(f"Output destination file is {out_path}")
