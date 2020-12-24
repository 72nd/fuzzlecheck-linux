#!/usr/bin/env python3

# Script to install Fuzzlecheck 4 on a Linux system based on the Mac Image.
#
# Use this script at your own risk. The author is in no way associated with
# the developers of Fuzzlecheck.

# Modify this constants to match your needs.
DESTINATION = "~/.local/bin/fuzzlecheck/"
APPLICATIONS_FOLDER = "~/.local/share/applications/"
ICONS_HICOLOR_FOLDER = "~/.local/share/icons/hicolor/"
GTK_THEME = "Adwaita"

# Internal constants, do not change.
IMG_JAVA_LOCATION = "Fuzzlecheck 4/Fuzzlecheck 4.app/Contents/Java"
IMG_ICON_LOCATION = "Fuzzlecheck 4/Fuzzlecheck 4.app/Contents/Resources/icon_mac.icns"
IMG_INFO_LOCATION = "Fuzzlecheck 4/Fuzzlecheck 4.app/Contents/Info.plist"
ICON_SIZES = [16, 24, 32, 48, 64, 128, 256, 512]
MANIFEST_TEMPLATE = """Manifest-Version: 1.0
JavaFX-Version: 8.0
Implementation-Version: {version}
Permissions: sandbox
Main-Class: com.fuzzlecheck.Fuzzlecheck
Implementation-Vendor: Milieufilm
{classpath}
"""
DESKTOP_TEMPLATE = """[Desktop Entry]
Version={version}
Name=Fuzzlecheck 4
GenericName=Film Preproduction
Comment=Scheduling your shoot has never been easier.
Exec={env}java -jar {path}
Icon=fuzzlecheck
Terminal=false
Type=Application
"""

import os
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
    subprocess.call(["convert", source_icon_path(temp_folder, 16), "-resize", "24x24", source_icon_path(temp_folder, 24)])
    subprocess.call(["convert", source_icon_path(temp_folder, 128), "-resize", "48x48", source_icon_path(temp_folder, 48)])
    subprocess.call(["convert", source_icon_path(temp_folder, 128), "-resize", "64x64", source_icon_path(temp_folder, 64)])

def inject_manifest(temp_folder: Path, application_folder: Path, version: str):
    """Generates and injects the manifest file into `Fuzzlecheck.jar`."""
    classpath = get_classpath(application_folder)
    content = MANIFEST_TEMPLATE.format(version = version, classpath = classpath)

    with zipfile.ZipFile(application_folder.joinpath("Fuzzlecheck.jar"), mode = 'a') as jar:
        jar.writestr("META-INF/MANIFEST.MF", content)

def get_fuzzlecheck_version(temp_folder: Path) -> str:
    """Parses the `Info.plist` file and returns the version number of Fuzzlecheck."""
    with open(temp_folder.joinpath(IMG_INFO_LOCATION)) as f:
        info = f.read()
    pattern = re.compile(r"<key>CFBundleVersion</key>\n<string>(.*)</string>")
    return pattern.search(info).group(1)

def get_classpath(application_folder: Path) -> str:
    """Returns the Class-Path for the JAR's manifest file. This is determined by reading the names of all JAR files in
    the application folder. A line in a manifest file is allowed to have a length of 72 bytes at max."""
    items  = []
    for item in application_folder.iterdir():
        items.append(item.name + " ")
    items = sorted(items)

    rsl = []
    line = "Class-Path: "
    for item in items:
        if item == "Fuzzlecheck.jar":
            continue
        for char in item:
            if len(line.encode("UTF-8")) == 70:
                rsl.append(line)
                line = " "
            line += char
    return "\n".join(rsl)

def install_application(application_folder: Path):
    """Copies the application folder to the given location."""
    destination = Path(DESTINATION).expanduser()
    if destination.exists():
        sys.exit("The destination folder {} already exists. Use `fuzzlecheck.py uninstall` to remove an existing installation.".format(destination))
    shutil.copytree(application_folder, destination)

def install_icons(temp_folder: Path):
    """Copies the extracted icons to the given hicolor icons location."""
    for size in ICON_SIZES:
        source = source_icon_path(temp_folder, size)
        destination = Path(ICONS_HICOLOR_FOLDER).expanduser().joinpath("{size}x{size}/apps/fuzzlecheck.png".format(size = size))
        shutil.copyfile(source, destination)

def install_desktop_file(version: str):
    """Writes the .desktop file to the applications folder."""
    env = ""
    if GTK_THEME != "":
        env = "env GTK_THEME={} ".format(GTK_THEME)
    path = Path(DESTINATION).expanduser().joinpath("Fuzzlecheck.jar")
    with open(desktop_file_path(), "w") as f:
        f.write(DESKTOP_TEMPLATE.format(version = version, env = env, path = path))

def source_icon_path(temp_folder: Path, size: int) -> Path:
    """Returns the temporary location for a given icon size."""
    return temp_folder.joinpath("icon_mac_{size}x{size}x32.png".format(size = size))

def desktop_file_path() -> Path:
    """Returns the path to the .desktop file."""
    return Path(APPLICATIONS_FOLDER).expanduser().joinpath("fuzzlecheck.desktop")

def uninstall_on_parameter():
    """Uninstalls Fuzzlecheck if the argument uninstall is given by the user."""
    if len(sys.argv) != 2 or sys.argv[1] != "uninstall":
        return

    # Application data
    shutil.rmtree(Path(DESTINATION).expanduser())

    # Icons
    for size in ICON_SIZES:
        os.remove(Path(ICONS_HICOLOR_FOLDER).expanduser().joinpath("{size}x{size}/apps/fuzzlecheck.png".format(size = size)))

    # Desktop entry
    os.remove(desktop_file_path())

    print("Fuzzlecheck was removed.")
    sys.exit(0)

if __name__ == "__main__":
    uninstall_on_parameter()

    temp_folder = TemporaryDirectory()
    temp_folder_path = Path(temp_folder.name)
    application_folder = temp_folder_path.joinpath("fuzzlecheck")

    img = get_img_path()
    extract_image(img, temp_folder_path)
    version = get_fuzzlecheck_version(temp_folder_path)

    build_application_folder(temp_folder_path, application_folder)
    build_icon(temp_folder_path)
    inject_manifest(temp_folder_path, application_folder, version)

    install_application(application_folder)
    install_icons(temp_folder_path)
    install_desktop_file(version)

    temp_folder.cleanup()


