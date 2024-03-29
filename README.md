# Fuzzlecheck for Linux

## Introduction 
 
[Fuzzlecheck](https://www.fuzzlecheck.de/index/EN/index.html) is a film preproduction management software which is quiet popular in Germany. Officially it only runs on Windows or Mac. But as it's only a bundled Java Application, it also runs on Linux. I've written a simple Python script to extract the files from the Mac Image and install them on your Linux box. Further a `.desktop` entry is added so you can use the application like any other.

**Disclaimer:** This software comes without any warranty. Be aware of the potential danger of loosing your (expensive) Fuzzlecheck software-key.


## Usage

### Perquisites 

You need to have the following packages installed on your System:

- _7z_ to extract the content of the Image.
- _Python 3_ to run the script itself.
- _Icnsutils_ to convert the icon for the desktop starter.
- _Imagemagick_ to scale the icons.
- _Java Runtime Environment 8_ for running the application in the end. Later JRE's won't work as Fuzzlecheck uses the (since JRE 9) depreciated `sun.util.calendar.ZoneInfo` class.

For Ubuntu:

```shell script
sudo apt install openjdk-8-jre p7zip-full python3 icnsutils
``` 

For Fedora:

```shell script
sudo dnf install java-1.8.0-openjdk p7zip-plugins python3 libicns-utils
```  

### Get the application image

Download the current Mac version of Fuzzlecheck from [here](http://fuz4downloads.fuzzlecheck.com/?linkOSX=Fuzzlecheck) and save it somewhere on your system.


### Run the script

Clone this repository.

```shell script
git clone https://github.com/72nd/fuzzlecheck-linux.git
cd fuzzlecheck-linux
```

You can change the installation destination by modifying the constant in the script file.

- `DESTINATION`. Path to the folder where the Fuzzlecheck folder will be copied to. Defaults to `~/.local/bin/fuzzlecheck/`.
- `APPLICATIONS_FOLDER`. Path to the applications folder where the `fuzzlecheck.desktop` will be created. Defaults to `~/.local/share/applications/`.
- `ICONS_HICOLOR_FOLDER`. Path to the location of the hicolor icon folder. Defaults to `~/.local/share/icons/hicolor/`
- `GTK_THEME`. Some GTK dark-themes clash with the interface of Fuzzlecheck if the constant isn't empty the application will be started with the given theme. Defaults to `Adwaita`.
- `JAVA_EXECUTABLE`. Path to the `java` executable for running the application. As Fuzzlecheck relies on JRE 8 (see above) you may specify this to the JRE 8 executable. Defaults to `/usr/lib/jvm/jre-1.8.0/bin/java`

Then run the script with the path to the Fuzzlecheck dmg image.

```shell script
./fuzzlecheck.py path/to/image/fuz_mac_setup_4.X.X.dmg
```

## Uninstall

You can remove Fuzzlecheck by calling

```shell script
.fuzzlecheck.py uninstall
```

## How does this works?

The Application bundles a number of Jar files which can be executed by any System the Jave Runtime is available. This script extracts the needed JAR files from the dmg file using 7z. It then generates a custom [Manifest File](https://docs.oracle.com/javase/tutorial/deployment/jar/manifestindex.html) which gets injected into the main JAR. Afterwards the application will be installed to your system and a application launcher (.desktop file) will be added.


# Todo

- [ ] Use argparse instead of constants in the scripts (as normal peoples tend to do).
- [ ] Use the [FlatLeafe](https://www.formdev.com/flatlaf/#download) theme.
