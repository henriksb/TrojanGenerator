# TrojanGenerator

Quickily turn any file into a trojan disguised as any filetype. To use TrojanGenerator, all you need to do is replace the value of PYINSTALLER_PATH (in TrojanGenerator.py) with the path of your pyinstaller installation, unless you have Anaconda for python 2.7 installed.

TrojanGenerator creates an executable which downloads two files, one file that will open and show, and another file (virus) that will open and run silently in the background. You can also spoof the extension and change icon to improve the authenticity.



### Usage:

##### Required:

* --frontfile: File URL. This will be the front file (the file being displayed).

* --backfile: File URL. This will be the back file (the virus running in the background).

* --name: Output name of file.

##### Optional:

* --real_extension: The real file extension. This can only be scr, com and exe.

* --spoof_extension:  Filetype the executable will appear as.

* --icon: Executable icon.

* --zip: Boolean. Zip file or not, not zipping by default.



### Requirements:

- pyinstaller for python 2.7






