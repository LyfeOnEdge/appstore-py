import os
import tkinter
import traceback
from tkinter import filedialog
from appstore import getPackage, parser, appstore_handler
from webhandler import getJson #getJson grabs json file with etagging

if not os.path.exists('downloads'):
	os.mkdir('downloads')

try:
	# Start tkinter then immediately close the root window, this
	# prevents a tkinter root window from popping up but lets tkinter 
	# run in the background so we can use its file dialog utility
	tkinter.Tk().withdraw() 

	packages_to_install = [
		"Atmosphere", #CFW
		"lennytube", #Youtube homebrew alternative
	]

	#Download the appstore team's repo with etagging
	repo = getJson('repo', 'https://www.switchbru.com/appstore/repo.json')
	repo_parser = parser()
	#Load the repo file
	repo_parser.load_file(repo)
	#Get the path to a switch SD card with a simple pop-up dialog
	chosensdpath = filedialog.askdirectory(initialdir="/",  title='Please select your SD card')
	#Handler for dealing with SD card contents
	store_handler = appstore_handler()
	#Set handler's working directory to the base directory of the SD card
	store_handler.set_path(chosensdpath)
	#Check if the appstore .get folder has been initiated here
	if not store_handler.check_if_get_init():
		store_handler.init_get()

	for package in packages_to_install:
		#Get the repo dict for each package by package name
		pkg = repo_parser.get_package(package)
		#Install the package (Downloads from the Appstore team's servers)
		store_handler.install_package(pkg)

	print("Installed packages - {}".format(packages_to_install))
except Exception as e:
	print(e)
	print(traceback.format_exc())
	with open("log.txt", 'w+') as log:
		log.write(traceback.format_exc())