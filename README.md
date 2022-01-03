# Musical-Images-generator

A Python script that generates images compatible with the 
[Musical-Images](https://github.com/UnsignedArduino/Musical-Images) extension
for MakeCode Arcade!

## Installation

1. Install Python 3.9 or newer
2. Download the code, either via `git clone` (You'll need `git` for that 
   obviously) or download via ZIP and extract to somewhere. 
3. Install the dependencies needed in 
   [`requirements.txt`](https://github.com/UnsignedArduino/Musical-Images-Generator/blob/main/requirements.txt)

## Usage

Run `main.py` and pass in a path to a MIDI file. A text file with MakeCode 
Arcade images should be in the same directory as the MIDI file. Open it using 
your favorite text editor and copy all the images into image blocks or 
an animation block in the MakeCode Arcade editor. The images will be limited to
512x88 (88 keys on piano) so you should make your animation/images that big. 
The last image will usually be smaller, which you can trim down to save space 
when compiling. 
