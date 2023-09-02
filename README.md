# Android-Debloater
[DOES NOT REQUIRE ROOT]

very simple script for automated debloating of android (meant for linux use only)

supports list like structure for debloating android ,installing apks and executing adb shell commands
## use:
use example
```shell
python3 Android-Debloater.py -i degoogle.txt -p true -a true -s true
```

usage
```
usage: Android-Debloater.py [-h] [-i INPUT] [-p PERMENANT] [-a ADD] [-s SHELL]

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        list of package names to be removed .txt format
  -p PERMENANT, --permenant PERMENANT
                        try to permenantly delete packages
  -a ADD, --add ADD     enable adding packages from list links
  -s SHELL, --shell SHELL
                        enable running shell commands from list
```
## run:
run degoole list
```shell
wget https://raw.githubusercontent.com/ChromiumOS-Guy/Android-Debloater/main/Android-Debloater.py && wget https://raw.githubusercontent.com/ChromiumOS-Guy/Android-Debloater/main/examples/degoogle.txt && python3 Android-Debloater.py -i degoogle.txt -p true -a true -s true
```

run degoogle and foss collection (gapp replacment) list
```shell
wget https://raw.githubusercontent.com/ChromiumOS-Guy/Android-Debloater/main/Android-Debloater.py && wget https://raw.githubusercontent.com/ChromiumOS-Guy/Android-Debloater/main/examples/degoogle.txt && python3 Android-Debloater.py -i degoogle_replace_with_foss.txt -p true -a true -s true
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
if you want to delete a bunch of android packages say all google packages you can use this command
```shell
adb shell pm list packages | grep google
```
