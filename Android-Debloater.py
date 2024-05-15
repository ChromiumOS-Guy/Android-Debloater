import os
import argparse
import shutil
import pathlib


LOGFILE = os.getcwd() + "/" + "android-debloat-log.txt" # get run Directory and make a log file path there
TEMP = os.getcwd() + "/" + ".temp" # make a temporary folder to house the temporary files
HERE = os.path.realpath(os.path.dirname(__file__)) # find script Directory

parser = argparse.ArgumentParser() # init argspace
parser.add_argument('-i' , '--input' , type=argparse.FileType('r') , help='''list of package names to be removed .txt format''')
parser.add_argument('-p' , '--permenant' , action='store_true', help='''try to permenantly delete packages''')
parser.add_argument('-a' , '--add' , action='store_true', help='''enable adding packages from list links''')
parser.add_argument('-s' , '--shell' , action='store_true', help='''enable running shell commands from list''')
args = parser.parse_args() # get flags

LISTPATH = os.path.realpath(args.input.name) # .txt file with instructions for script to continue

packages_removed_permenant = [] # packages attemted to remove with root perms permenantly 
packages_removed_user = [] # packages attempted to remove with user perms temporarly
packages_failed_remove = [] # packages that script has failed to remove
packages_downloaded_installed = [] # packages script has downloaded and installed on phone



def remove_package(package_name : str , try_permenant : bool): # remove package function
	err = ""
	os.system("echo REMOVING '({package_name})' >> {LOGFILE}".format(package_name=package_name ,LOGFILE=LOGFILE)) # log package to be removed
	if try_permenant: # if user wants to try permenant try
		err = os.system("adb shell pm uninstall {package_name} >> {LOGFILE}".format(package_name=package_name ,LOGFILE=LOGFILE)) # try to uninstall package and log it to logfile
		if err == 0: # then try to remove it with user perms
			err = os.system("adb shell pm uninstall --user 0 {package_name} >> {LOGFILE}".format(package_name=package_name ,LOGFILE=LOGFILE))
			if err == 0: # if succeded in removing it with user perms after removing with root perms that means we failed at removing it permenantly so we append it to user removed packages
				packages_removed_user.append(package_name)
			else: # else we append it to root removed packages
				packages_removed_permenant.append(package_name)
		if err != 0: # if it completly failed to even try to remove it with root perms then fall back to user perms
			os.system("echo ===FALLING BACK TO USER ONLY!!!=== >> {LOGFILE}".format(package_name=package_name ,LOGFILE=LOGFILE)) # log fallback
			err = os.system("adb shell pm uninstall --user 0 {package_name} >> {LOGFILE}".format(package_name=package_name ,LOGFILE=LOGFILE)) # log uninstall attempt & uninstall
			if err == 0: # append if succeded
				packages_removed_user.append(package_name)
	else: # if user wants to use user perms then do this
		err = os.system("adb shell pm uninstall --user 0 {package_name} >> {LOGFILE}".format(package_name=package_name ,LOGFILE=LOGFILE)) # log uninstall attempt & uninstall
		if err == 0: # append to user removed packges
			packages_removed_user.append(package_name)
	if err != 0: # if nothing worked then append failed to uninstall packages
		packages_failed_remove.append(package_name)
	os.system("echo '\n' >> {LOGFILE}".format(package_name=package_name ,LOGFILE=LOGFILE))

def download_package(package_link : str): # download packages online
	os.system("echo DOWNLOADING FROM LINK '({package_link})' >> {LOGFILE}".format(package_link=package_link ,LOGFILE=LOGFILE)) # log download link
	os.system("wget -c {package_link} -P {TEMP} -a {LOGFILE}".format(package_link=package_link ,LOGFILE=LOGFILE, TEMP=TEMP)) # log download & download
	os.system("echo '\n' >> {LOGFILE}".format(LOGFILE=LOGFILE))

def install_downloaded_packages(): # install downloaded packages
	APKS = os.listdir(TEMP) # list packages in TEMP Directory
	i = 0
	for apk in APKS:
		err = os.system("adb install {APK} >> {LOGFILE}".format(APK=os.path.realpath(TEMP + "/" + APKS[i]) ,LOGFILE=LOGFILE)) # log install attempt & install
		os.system("rm -rf {APK} >> {LOGFILE}".format(APK=os.path.realpath(TEMP + "/" + APKS[i]) ,LOGFILE=LOGFILE)) # log package deletion from script host
		if err == 0: # if succeded then append packages to downaloded & installed packages
			packages_downloaded_installed.append(APKS[i])
		i += 1

donextline = []
def parse_package_list(): # LISTPATH parser
	LIST = open(LISTPATH, 'r') # open .txt file
	packages = LIST.readlines() # read lines
	for package in packages: # iterate LISTPATH lines
		if package.strip().startswith("download:") and args.add and len(donextline) == 0: # if line starts with prefix download: then run download_package() function
			download_package(package.strip().split(":" ,1)[-1])
		elif package.strip().startswith("package:") and len(donextline) == 0: # if line starts with prefix package: then run remove_package() function
			remove_package(package.strip().split(":" ,1)[-1], args.permenant)
		elif package.strip().startswith("!package:") and len(donextline) == 0: # if line starts with perfix !package: then run remove_package() function with try_permenant as false
			remove_package(package.strip().split(":" ,1)[-1], False)
		elif package.strip().startswith("shell:") and len(donextline) == 0: # if line starts with prefix shell: then run shell command on the phone (like reboot)
			if args.shell: # run shell commands only if shell argument is True
				os.system("adb shell {command} >> {LOGFILE}".format(command=package.strip().split(":" ,1)[-1] ,LOGFILE=LOGFILE)) # run shell commmand and log it to logfile
			else: # skip if shell Argument is False
				pass
		elif package.strip() == "installpkgs": # if line starts and ends with the keywords installpkgs then run install_downloaded_packages() function
			install_downloaded_packages()
		elif package.strip().startswith("question:") and len(donextline) == 0: # if line starts with prefix question: then promet user for Yes No question
			answer = input(package.strip().split(":")[-1] + " (Y/n):" ) # promet user for Y/n Question with question text being last perfix of : represented by [-1]
			if answer == "y" or answer == "Y" or answer == "Yes" or answer == "yes" or answer == "": # if option selected line after will continue
				pass
			else: # else skip designated lines with the doneextline array
				for i in range(int(package.strip().split(":")[1])): 
					donextline.append("")
		elif package.strip().startswith("##"): # if prefix is ## than it is a comment is LISTPATH file
			pass
		else:
			if len(donextline) == 0: # if donextline == 0 than print the line
				print(package.strip())
			else: # if it isn't pop one
				donextline.pop()



def print_results(): # prints results for user to read
	total = len(packages_failed_remove) + len(packages_removed_user) + len(packages_removed_permenant) + len(packages_downloaded_installed) # calculate total packages remove/installed/failed_to_remove
	print("====================================")
	print("{total}/{permenant} permenantly removed".format(total=total , permenant=len(packages_removed_permenant)))
	print("{total}/{user_only} user only removed".format(total=total , user_only=len(packages_removed_user)))
	print("{total}/{downloaded_installed} downloaded and installed".format(total=total , downloaded_installed=len(packages_downloaded_installed)))
	print("{total}/{failed_remove} failed to remove".format(total=total , failed_remove=len(packages_failed_remove)))
	print("====================================")
	print("check log for more details")

def log_results():# log results in log file with bigger verbosity
	os.system("echo '\n' >> {LOGFILE}".format(LOGFILE=LOGFILE))
	if len(packages_removed_permenant) != 0: # start code if we removed packages permenantly
		os.system("echo '=======================================' >> {LOGFILE}".format(LOGFILE=LOGFILE))
		os.system("echo '     packages permenantly removed' >> {LOGFILE}".format(LOGFILE=LOGFILE))
		os.system("echo '=======================================' >> {LOGFILE}".format(LOGFILE=LOGFILE))
		for package in packages_removed_permenant:
			os.system("echo {package} >> {LOGFILE}".format(LOGFILE=LOGFILE, package=package)) # log package in array
	if len(packages_removed_user) != 0: # start code if we removed packages temporarly
		os.system("echo '=======================================' >> {LOGFILE}".format(LOGFILE=LOGFILE))
		os.system("echo '      packages user only removed' >> {LOGFILE}".format(LOGFILE=LOGFILE))
		os.system("echo '=======================================' >> {LOGFILE}".format(LOGFILE=LOGFILE))
		for package in packages_removed_user:
			os.system("echo {package} >> {LOGFILE}".format(LOGFILE=LOGFILE, package=package)) # log package in array
	if len(packages_downloaded_installed) != 0:  # start code if we installed packages
		os.system("echo '=======================================' >> {LOGFILE}".format(LOGFILE=LOGFILE))
		os.system("echo '   packages downloaded and installed' >> {LOGFILE}".format(LOGFILE=LOGFILE))
		os.system("echo '=======================================' >> {LOGFILE}".format(LOGFILE=LOGFILE))
		for package in packages_downloaded_installed:
			os.system("echo {package} >> {LOGFILE}".format(LOGFILE=LOGFILE, package=package)) # log package in array
	if len(packages_failed_remove) != 0:  # start code if we failed to removed packages
		os.system("echo '=======================================' >> {LOGFILE}".format(LOGFILE=LOGFILE))
		os.system("echo '       packages failed to remove' >> {LOGFILE}".format(LOGFILE=LOGFILE))
		os.system("echo '=======================================' >> {LOGFILE}".format(LOGFILE=LOGFILE))
		for package in packages_failed_remove:
			os.system("echo {package} >> {LOGFILE}".format(LOGFILE=LOGFILE, package=package)) # log package in array


def main(): # script main()
	os.system("mv {LOGFILE} {LOGFILE}.old && rm -rf {LOGFILE} >> {LOGFILE}".format(LOGFILE=LOGFILE)) # if log already exists then move it to .old and log action to new logfile
	os.system("mkdir {dir} >> {LOGFILE}".format(dir=TEMP ,LOGFILE=LOGFILE)) # make TEMP Directory
	parse_package_list() # start LISTPATH Parser which in turn removes & downloads/installs packages
	if len(os.listdir(TEMP)) != 0: # if packages where downloaded but not installed this failsafe will install them
		install_downloaded_packages()
	log_results() # log results in log file with bigger verbosity
	print_results() # prints results for user to read
	os.system("rm -rf {dir}".format(dir=TEMP)) # deletes TEMP Directory
main() # start script main()
