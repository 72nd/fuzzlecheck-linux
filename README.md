# Fuzzlecheck for Linux

## Introduction 
 
[Fuzzlecheck](https://www.fuzzlecheck.de/index/EN/index.html) is a film preproduction management software which is quiet popular in Germany. Officially it only runs on Windows or Mac. But as it's only a bundled Java Application, it can also runs on Linux. I've written a simple Python script to extract the files from the Mac Image and install them on your Linux box.


## Usage

### Perquisites 

You need to have the following packages installed on your System:

- _7z_ to extract the content of the Image.
- _Python 3_ to run the script itself.
- _Icnsutils_ to convert the icon for the desktop starter.
- A current version of the _Java Runtime Environment_ (OpenJDK JRE 14 works for me) to run Fuzzlecheck in the end.

For Ubuntu:

```shell script
sudo apt install openjdk-14-jre p7zip-full python3 icnsutils
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

- `DESTINATION`. Path to the folder where the Fuzzlecheck files will be copied to. Defaults to `~/.local/bin/fuzzlecheck/`.
- `APPLICATIONS_FOLDER`. Path to the applications folder where the `fuzzlecheck.desktop` will be created. Defaults to `~/.local/share/applications/`.

Then run the script with the path to the Fuzzlecheck dmg image.

```shell script
./fuzzlecheck.py path/to/image/fuz_mac_setup_4.X.X.dmg
```

## How does this works?

The Application bundles a number of Jar files which can be executed by any System the Jave Runtime is available. This script extracts the needed JAR files from the dmg file using 7z. It then generates a custom [Manifest File](https://docs.oracle.com/javase/tutorial/deployment/jar/manifestindex.html) which gets injected into the main JAR. Afterwards the application will be installed to your system and a application launcher (.desktop file) will be added.


