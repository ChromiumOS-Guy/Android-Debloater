import os
import argparse

LOGFILE = os.getcwd() + "/" + "android-debloat-log.txt"
TEMP = os.getcwd() + "/" + ".temp"
HERE = os.path.realpath(os.path.dirname(__file__))

parser = argparse.ArgumentParser()
parser.add_argument('-i' , '--input' , type=argparse.FileType('r') , help='''list of package names to be removed .txt format''')
parser.add_argument('-p' , '--permenant' , type=bool , help='''try to permenantly delete packages''')
parser.add_argument('-a' , '--add' , type=bool , help='''enable adding packages from list links''')
args = parser.parse_args()

LISTPATH = os.path.realpath(args.input.name)
try_permenant = args.permenant
add = args.add

packages_removed_permenant = []
packages_removed_user = []
packages_failed_remove = []
packages_downloaded = []
packages_installed = []



def remove_package(package_name : str):
	err = ""
	os.system("echo REMOVING '({package_name})' >> {LOGFILE}".format(package_name=package_name ,LOGFILE=LOGFILE))
	if try_permenant:
		err = os.system("adb uninstall {package_name} >> {LOGFILE}".format(package_name=package_name ,LOGFILE=LOGFILE))
		if err == 0:
			packages_removed_permenant.append(package_name)
		if err != 0:
			os.system("echo ===FALLING BACK TO USER ONLY!!!=== >> {LOGFILE}".format(package_name=package_name ,LOGFILE=LOGFILE))
			err = os.system("adb uninstall --user 0 {package_name} >> {LOGFILE}".format(package_name=package_name ,LOGFILE=LOGFILE))
			if err == 0:
				packages_removed_user.append(package_name)
	else:
		err = os.system("adb uninstall --user 0 {package_name} >> {LOGFILE}".format(package_name=package_name ,LOGFILE=LOGFILE))
		if err == 0:
			packages_removed_user.append(package_name)
	if err != 0:
		packages_failed_remove.append(package_name)
	os.system("echo '\n' >> {LOGFILE}".format(package_name=package_name ,LOGFILE=LOGFILE))

def download_package(package_link : str):
	err = ""
	os.system("echo DOWNLOADING FROM LINK '({package_link})' >> {LOGFILE}".format(package_link=package_link ,LOGFILE=LOGFILE))
	err = os.system("wget -c {package_link} -P {TEMP} -a {LOGFILE}".format(package_link=package_link ,LOGFILE=LOGFILE, TEMP=TEMP))
	if err != 0:
		packages_downloaded.append(package_link)
	os.system("echo '\n' >> {LOGFILE}".format(LOGFILE=LOGFILE))

def install_downloaded_packages():
	APKS = os.listdir(TEMP)
	i = 0
	err = ""
	for apk in APKS:
            err = os.system("adb install {APK} >> {LOGFILE}".format(APK=os.path.realpath(TEMP + "/" + APKS[i]) ,LOGFILE=LOGFILE))
            if err == None:
            	packages_installed.append(APKS[i])
            i += 1

def parse_package_list():
	LIST = open(LISTPATH, 'r')
	packages = LIST.readlines()
	for package in packages:
		if package.strip().startswith("http") and add:
			download_package(package.strip())
		elif package.strip().startswith("##"):
			pass
		else:
			remove_package(package.strip())


def print_results():
	total = len(packages_failed_remove) + len(packages_removed_user) + len(packages_removed_permenant) + len(packages_downloaded) + len(packages_installed)
	print("===========================")
	if len(packages_removed_permenant) != 0:
		print("{total}/{permenant} permenantly removed".format(total=total , permenant=len(packages_removed_permenant)))
	if len(packages_removed_user) != 0:
		print("{total}/{user_only} user only removed".format(total=total , user_only=len(packages_removed_user)))
	if len(packages_downloaded) != 0:
		print("{total}/{downloaded} downloaded".format(total=total , downloaded=len(packages_downloaded)))
	if len(packages_installed) != 0:
		print("{total}/{installed} installed".format(total=total , installed=len(packages_installed)))
	if len(packages_failed_remove) != 0:
		print("{total}/{failed_remove} failed to remove".format(total=total , failed_remove=len(packages_failed_remove)))
	print("===========================")
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
	if len(packages_downloaded) != 0:
		os.system("echo '=======================================' >> {LOGFILE}".format(LOGFILE=LOGFILE))
		os.system("echo '      	 packages downloaded' >> {LOGFILE}".format(LOGFILE=LOGFILE))
		os.system("echo '=======================================' >> {LOGFILE}".format(LOGFILE=LOGFILE))
		for package in packages_downloaded:
			os.system("echo {package} >> {LOGFILE}".format(LOGFILE=LOGFILE, package=package))
	if len(packages_installed) != 0:
		os.system("echo '=======================================' >> {LOGFILE}".format(LOGFILE=LOGFILE))
		os.system("echo '          packages installed' >> {LOGFILE}".format(LOGFILE=LOGFILE))
		os.system("echo '=======================================' >> {LOGFILE}".format(LOGFILE=LOGFILE))
		for package in packages_installed:
			os.system("echo {package} >> {LOGFILE}".format(LOGFILE=LOGFILE, package=package))
	if len(packages_failed_remove) != 0:
		os.system("echo '=======================================' >> {LOGFILE}".format(LOGFILE=LOGFILE))
		os.system("echo '       packages failed to remove' >> {LOGFILE}".format(LOGFILE=LOGFILE))
		os.system("echo '=======================================' >> {LOGFILE}".format(LOGFILE=LOGFILE))
		for package in packages_failed_remove:
			os.system("echo {package} >> {LOGFILE}".format(LOGFILE=LOGFILE, package=package))


def main():
	os.system("mkdir {dir}".format(dir=TEMP))
	os.system("mv {LOGFILE} {LOGFILE}.old".format(LOGFILE=LOGFILE))
	os.system("rm -rf {LOGFILE}".format(LOGFILE=LOGFILE))
	parse_package_list()
	install_downloaded_packages()
	log_results()
	print_results()
	os.system("rm -rf {dir}".format(dir=TEMP))
main()
