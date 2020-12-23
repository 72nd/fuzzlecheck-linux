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
IMG_INFO_LOCATION = "Fuzzlecheck 4/Fuzzlecheck 4.app/Contents/Info.plist"
MANIFEST_TEMPLATE = """Manifest-Version: 1.0
JavaFX-Version: 8.0
Implementation-Version: {version}
Permissions: sandbox
Main-Class: com.fuzzlecheck.Fuzzlecheck
Implementation-Vendor: Milieufilm
Class-Path: {classpath}
"""

from pathlib import Path
import re
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory
from typing import List
import zipfile

def get_img_path() -> Path:
    """Gets the path of the Mac installation image from the command line arguments. Fails
    with an error if the argument is not present or the given file doesn't exist."""
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
    """Uses 7z to extract the content of the dmg file into the temporary folder."""
    try:
        subprocess.check_output(["7z", "x", img, "-o{}".format(temp_folder)])
    except subprocess.CalledProcessError as e:
        print("Some error occurred while the execution of 7z. \"HFS Headers Errors\" can be ignored.\n---{}\n---".format(e.output))

def build_application_folder(temp_folder: Path, application_folder: Path):
    """Copies the relevant files into the fuzzlecheck folder in the temporary folder."""
    java_folder = temp_folder.joinpath(Path(IMG_JAVA_LOCATION))
    shutil.copytree(java_folder, application_folder)
    print(java_folder)

def build_icon(temp_folder: Path):
    """Extracts the different icons sizes."""
    source = temp_folder.joinpath(Path(IMG_ICON_LOCATION))
    try:
        subprocess.check_output(["icns2png", "-x", source, "-o", temp_folder])
    except subprocess.CalledProcessError as e:
        sys.exit(e.output)

def inject_manifest(temp_folder: Path, application_folder: Path):
    """Generates and injects the manifest file into `Fuzzlecheck.jar`."""
    version = get_fuzzlecheck_version(temp_folder)
    jars = get_jars(application_folder)
    content = MANIFEST_TEMPLATE.format(version = version, classpath = " ".join(jars))

    with zipfile.ZipFile(application_folder.joinpath("Fuzzlecheck.jar"), mode = 'a') as jar:
        jar.writestr("META-INF/MANIFEST.MF", content)

def get_fuzzlecheck_version(temp_folder: Path) -> str:
    """Parses the `Info.plist` file and returns the version number of Fuzzlecheck."""
    with open(temp_folder.joinpath(IMG_INFO_LOCATION)) as f:
        info = f.read()
    pattern = re.compile(r"<key>CFBundleVersion</key>\n<string>(.*)</string>")
    return pattern.search(info).group(1)

def get_jars(application_folder: Path) -> List[str]:
    """Returns a list with all JAR files in the application folder. Used to generate the Class-Path
    in the manifest file."""
    rsl = []
    for item in application_folder.iterdir():
        rsl.append(item.name)
    return rsl

if __name__ == "__main__":
    temp_folder = TemporaryDirectory()
    temp_folder_path = Path(temp_folder.name)
    application_folder = temp_folder_path.joinpath("fuzzlecheck")

    img = get_img_path()
    extract_image(img, temp_folder_path)
    build_application_folder(temp_folder_path, application_folder)
    build_icon(temp_folder_path)
    inject_manifest(temp_folder_path, application_folder)

    input()
    temp_folder.cleanup()


