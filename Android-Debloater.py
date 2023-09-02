import os
import argparse
import shutil
import pathlib

LOGFILE = os.getcwd() + "/" + "android-debloat-log.txt"
TEMP = os.getcwd() + "/" + ".temp"
HERE = os.path.realpath(os.path.dirname(__file__))

parser = argparse.ArgumentParser()
parser.add_argument('-i' , '--input' , type=argparse.FileType('r') , help='''list of package names to be removed .txt format''')
parser.add_argument('-p' , '--permenant' , type=bool , help='''try to permenantly delete packages''')
parser.add_argument('-a' , '--add' , type=bool , help='''enable adding packages from list links''')
parser.add_argument('-s' , '--shell' , type=bool , help='''enable running shell commands from list''')
args = parser.parse_args()

LISTPATH = os.path.realpath(args.input.name)

packages_removed_permenant = []
packages_removed_user = []
packages_failed_remove = []
packages_downloaded_installed = []



def remove_package(package_name : str , try_permenant : bool):
	err = ""
	os.system("echo REMOVING '({package_name})' >> {LOGFILE}".format(package_name=package_name ,LOGFILE=LOGFILE))
	if try_permenant:
		err = os.system("adb shell pm uninstall {package_name} >> {LOGFILE}".format(package_name=package_name ,LOGFILE=LOGFILE))
		if err == 0:
			packages_removed_permenant.append(package_name)
		if err != 0:
			os.system("echo ===FALLING BACK TO USER ONLY!!!=== >> {LOGFILE}".format(package_name=package_name ,LOGFILE=LOGFILE))
			err = os.system("adb shell pm uninstall --user 0 {package_name} >> {LOGFILE}".format(package_name=package_name ,LOGFILE=LOGFILE))
			if err == 0:
				packages_removed_user.append(package_name)
	else:
		err = os.system("adb shell pm uninstall --user 0 {package_name} >> {LOGFILE}".format(package_name=package_name ,LOGFILE=LOGFILE))
		if err == 0:
			packages_removed_user.append(package_name)
	if err != 0:
		packages_failed_remove.append(package_name)
	os.system("echo '\n' >> {LOGFILE}".format(package_name=package_name ,LOGFILE=LOGFILE))

def download_package(package_link : str):
	os.system("echo DOWNLOADING FROM LINK '({package_link})' >> {LOGFILE}".format(package_link=package_link ,LOGFILE=LOGFILE))
	os.system("wget -c {package_link} -P {TEMP} -a {LOGFILE}".format(package_link=package_link ,LOGFILE=LOGFILE, TEMP=TEMP))
	os.system("echo '\n' >> {LOGFILE}".format(LOGFILE=LOGFILE))

def install_downloaded_packages():
	APKS = os.listdir(TEMP)
	i = 0
	for apk in APKS:
		err = os.system("adb install {APK} >> {LOGFILE}".format(APK=os.path.realpath(TEMP + "/" + APKS[i]) ,LOGFILE=LOGFILE))
		os.system("rm -rf {APK} >> {LOGFILE}".format(APK=os.path.realpath(TEMP + "/" + APKS[i]) ,LOGFILE=LOGFILE))
		if err == 0:
			packages_downloaded_installed.append(APKS[i])
		i += 1

donextline = []
def parse_package_list():
	LIST = open(LISTPATH, 'r')
	packages = LIST.readlines()
	for package in packages:
		if package.strip().startswith("download:") and args.add and len(donextline) == 0:
			download_package(package.strip().split(":" ,1)[-1])
		elif package.strip().startswith("package:") and len(donextline) == 0:
			remove_package(package.strip().split(":" ,1)[-1], args.permenant)
		elif package.strip().startswith("!package:") and len(donextline) == 0:
			remove_package(package.strip().split(":" ,1)[-1], False)
		elif package.strip().startswith("shell:") and len(donextline) == 0:
			if args.shell:
				os.system("adb shell {command} >> {LOGFILE}".format(command=package.strip().split(":" ,1)[-1] ,LOGFILE=LOGFILE))
			else:
				pass
		elif package.strip() == "installpkgs":
			install_downloaded_packages()
		elif package.strip().startswith("question:") and len(donextline) == 0:
			answer = input(package.strip().split(":")[-1] + " (Y/n):" )
			if answer == "y" or answer == "Y" or answer == "Yes" or answer == "yes" or answer == "":
				pass
			else:
				for i in range(int(package.strip().split(":")[1])):
					donextline.append("")
		elif package.strip().startswith("##"):
			pass
		else:
			if len(donextline) == 0:
				print(package.strip())
			else:
				donextline.pop()



def print_results():
	total = len(packages_failed_remove) + len(packages_removed_user) + len(packages_removed_permenant) + len(packages_downloaded_installed)
	print("====================================")
	print("{total}/{permenant} permenantly removed".format(total=total , permenant=len(packages_removed_permenant)))
	print("{total}/{user_only} user only removed".format(total=total , user_only=len(packages_removed_user)))
	print("{total}/{downloaded_installed} downloaded and installed".format(total=total , downloaded_installed=len(packages_downloaded_installed)))
	print("{total}/{failed_remove} failed to remove".format(total=total , failed_remove=len(packages_failed_remove)))
	print("====================================")
	print("check log for more details")

def log_results():
	os.system("echo '\n' >> {LOGFILE}".format(LOGFILE=LOGFILE))
	if len(packages_removed_permenant) != 0:
		os.system("echo '=======================================' >> {LOGFILE}".format(LOGFILE=LOGFILE))
		os.system("echo '     packages permenantly removed' >> {LOGFILE}".format(LOGFILE=LOGFILE))
		os.system("echo '=======================================' >> {LOGFILE}".format(LOGFILE=LOGFILE))
		for package in packages_removed_permenant:
			os.system("echo {package} >> {LOGFILE}".format(LOGFILE=LOGFILE, package=package))
	if len(packages_removed_user) != 0:
		os.system("echo '=======================================' >> {LOGFILE}".format(LOGFILE=LOGFILE))
		os.system("echo '      packages user only removed' >> {LOGFILE}".format(LOGFILE=LOGFILE))
		os.system("echo '=======================================' >> {LOGFILE}".format(LOGFILE=LOGFILE))
		for package in packages_removed_user:
			os.system("echo {package} >> {LOGFILE}".format(LOGFILE=LOGFILE, package=package))
	if len(packages_downloaded_installed) != 0:
		os.system("echo '=======================================' >> {LOGFILE}".format(LOGFILE=LOGFILE))
		os.system("echo '   packages downloaded and installed' >> {LOGFILE}".format(LOGFILE=LOGFILE))
		os.system("echo '=======================================' >> {LOGFILE}".format(LOGFILE=LOGFILE))
		for package in packages_downloaded_installed:
			os.system("echo {package} >> {LOGFILE}".format(LOGFILE=LOGFILE, package=package))
	if len(packages_failed_remove) != 0:
		os.system("echo '=======================================' >> {LOGFILE}".format(LOGFILE=LOGFILE))
		os.system("echo '       packages failed to remove' >> {LOGFILE}".format(LOGFILE=LOGFILE))
		os.system("echo '=======================================' >> {LOGFILE}".format(LOGFILE=LOGFILE))
		for package in packages_failed_remove:
			os.system("echo {package} >> {LOGFILE}".format(LOGFILE=LOGFILE, package=package))


def main():
	os.system("mv {LOGFILE} {LOGFILE}.old && rm -rf {LOGFILE} >> {LOGFILE}".format(LOGFILE=LOGFILE))
	os.system("mkdir {dir} >> {LOGFILE}".format(dir=TEMP ,LOGFILE=LOGFILE))
	parse_package_list()
	if len(os.listdir(TEMP)) != 0:
		install_downloaded_packages()
	log_results()
	print_results()
	os.system("rm -rf {dir}".format(dir=TEMP))
main()
