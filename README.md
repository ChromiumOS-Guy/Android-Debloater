# Android-Debloater
[DOES NOT REQUIRE ROOT]

very simple script for automated debloating of android (meant for linux use only)
question
supports list like structure for debloating android ,installing apks and executing adb shell commands

requires wget & adb
## use:
use example
```shell
python3 Android-Debloater.py -i degoogle.txt -p -a -s
```

usage
```
usage: Android-Debloater.py [-h] [-i INPUT] [-p] [-a] [-s]

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        list of package names to be removed .txt format
  -p, --permenant       try to permenantly delete packages
  -a, --add             enable adding packages from list links
  -s, --shell           enable running shell commands from list
```
## run (non permenant):
run degoogle list
```shell
wget https://raw.githubusercontent.com/ChromiumOS-Guy/Android-Debloater/main/Android-Debloater.py && wget https://raw.githubusercontent.com/ChromiumOS-Guy/Android-Debloater/main/examples/degoogle.txt && python3 Android-Debloater.py -i degoogle.txt -a -s && rm -rf Android-Debloater.py && rm -rf degoogle.txt
```

run foss collection (gapp replacment) list
```shell
wget https://raw.githubusercontent.com/ChromiumOS-Guy/Android-Debloater/main/Android-Debloater.py && wget https://raw.githubusercontent.com/ChromiumOS-Guy/Android-Debloater/main/examples/foss_collection.txt && python3 Android-Debloater.py -i foss_collection.txt -a -s && rm -rf Android-Debloater.py && rm -rf foss_collection.txt
```

run Xiaomi Debloat list
```shell
wget https://raw.githubusercontent.com/ChromiumOS-Guy/Android-Debloater/main/Android-Debloater.py && wget https://raw.githubusercontent.com/ChromiumOS-Guy/Android-Debloater/main/examples/Xiaomi_Debloat.txt && python3 Android-Debloater.py -i Xiaomi_Debloat.txt -a -s && rm -rf Android-Debloater.py && rm -rf Xiaomi_Debloat.txt
```

## list syntax:
SYNTAX | MEANING | EXAMPLE
------------- | ------------- | -------------
package: | defines an android package | package:com.android.vending
!package: | defines an android package and forces to remove it with user only mode | !package:com.android.vending
download: | download an apk from the internet | download:https://f-droid.org/F-Droid.apk
shell: | android shell command | shell:reboot
question:n: | question to user, n is for number of lines after question to be affected if user answer is no said lines after question won't be used, question defualt is yes | question:1:reboot?
installpkgs | install all downloaded packages to phone | installpkgs
*##* | list comments | ##comment about list


## tips:
if you want to search a bunch of android packages on you're phone say all google packages you can use this command to list all packages with google in there name (on linux)
```shell
adb shell pm list packages | grep google
```
