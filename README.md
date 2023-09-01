# Android-Debloater
very simple script for automated debloating of android (meant for linux use only)
## features:
supports list like structure for debloating android and installing apks
## use:
use example
```shell
python3 Android-Debloater.py -i degoogle.txt -p true -a true
```

usage
```
usage: Android-Debloater.py [-h] [-i INPUT] [-p PERMENANT] [-a ADD]

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        list of package names to be removed .txt format
  -p PERMENANT, --permenant PERMENANT
                        try to permenantly delete packages
  -a ADD, --add ADD     enable adding packages from list links
```

## tip:
if you want to delete a bunch of android packages say all google packages you can use this command
```shell
adb shell pm list packages | grep google | cut -c 9-
```

if you want to make you're own list instead of the example degoogle.txt list the important thing to know about list syntax is:

com.* is android packages to be uninstalled

http* is ipv4 to download apk (keep in mind it uses wget and has to download an .apk file)

*##* is for comments
