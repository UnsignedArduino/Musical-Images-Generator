from argparse import ArgumentParser
from pathlib import Path

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
                         "instead of writing to a file. No info messages "
                         "will be written. ")
args = parser.parse_args()

in_path = args.path.expanduser().resolve()
out_path = args.output_path
to_stdout = args.stdout
if out_path is None:
    out_path = in_path.parent / (in_path.stem + ".txt")

if not to_stdout:
    print(f"Path to MIDI file is {in_path}")

# Parse here

if not to_stdout:
    print(f"Output destination file is {out_path}")
