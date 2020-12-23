#!/usr/bin/env python3

# Script to install Fuzzlecheck 4 on a Linux system based on the Mac Image.
#
# Use this script at your own risk. The author is in no way associated with
# the developers of Fuzzlecheck.

# Modify this constants to match your needs.
DESTINATION = "~/.local/bin/fuzzlecheck/"
APPLICATIONS_FOLDER = "~/.local/share/applications/"

# Internal constants, do not change.
IMG_JAVA_LOCATION = "Fuzzlecheck 4/Fuzzlecheck 4.app/Contents/Java"
IMG_ICON_LOCATION = "Fuzzlecheck 4/Fuzzlecheck 4.app/Contents/Resources/icon_mac.icns"

from pathlib import Path
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory

def get_img_path() -> Path:
    args = sys.argv
    if len(args) < 2:
        sys.exit("Please provide the path to the Fuzzlecheck image as argument.")
    if len(args) > 2:
        sys.exit("More arguments provided than needed")
    rsl = Path(args[1])
    if not rsl.exists():
        sys.exit("Given dmg image ({}) doesn't exist.".format(args[1]))
    return rsl

def extract_image(img: Path, temp_folder: Path):
    try:
        subprocess.check_output(["7z", "x", img, "-o{}".format(temp_folder)])
    except subprocess.CalledProcessError as e:
        print("Some error occurred while the execution of 7z. \"HFS Headers Errors\" can be ignored.\n---{}\n---".format(e.output))

def build_application_folder(temp_folder: Path, application_folder: Path):
    java_folder = temp_folder.joinpath(Path(IMG_JAVA_LOCATION))
    shutil.copytree(java_folder, application_folder)
    print(java_folder)

def build_icon(temp_folder: Path):
    source = temp_folder.joinpath(Path(IMG_ICON_LOCATION))
    try:
        subprocess.check_output(["icns2png", "-x", source, "-o", temp_folder])
    except subprocess.CalledProcessError as e:
        sys.exit(e.output)


if __name__ == "__main__":
    temp_folder = TemporaryDirectory()
    temp_folder_path = Path(temp_folder.name)
    application_folder = temp_folder_path.joinpath("fuzzlecheck")
    print(temp_folder)

    img = get_img_path()
    extract_image(img, temp_folder_path)
    build_application_folder(temp_folder_path, application_folder)
    build_icon(temp_folder_path)

    input()
    temp_folder.cleanup()


