# Android-Debloater
very simple script for automated debloating of android (meant for linux use only)
## features:
supports list like structure for debloating android and installing apks
## use:
use
```shell
python3 Android-Debloater.py -i degoogle.txt -p -a
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
