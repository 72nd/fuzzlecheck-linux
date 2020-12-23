#!/usr/bin/env python3

# Script to install Fuzzlecheck 4 on a Linux system based on the Mac Image.
#
# Use this script at your own risk. The author is in no way associated with
# the developers of Fuzzlecheck.

# Modify this constants to match your needs.
DESTINATION = "~/.local/bin/fuzzlecheck/"
APPLICATIONS_FOLDER = "~/.local/share/applications/"

import sys
from pathlib import Path

def get_img_path() -> Path:
    args = sys.argv
    if len(args) < 2:
        sys.exit("Please provide the path to the Fuzzlecheck image as argument.")
    if len(args) > 2:
        sys.exit("More arguments provided than needed")
    rsl = Path(args[1])
    if not rsl.exists():
        sys.exit("Given input image ({}) doesn't exist.".format(args[1]))
    return rsl

if __name__ == "__main__":
    img = get_img_path()
    print(img)


