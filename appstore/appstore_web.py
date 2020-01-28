#Some basic scripts for grabbing icon and screenshot for packages using the appstore site.
#Copyright LyfeOnEdge 2019
#Licensed under GPL3
import sys, os

import urllib.request 
opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
urllib.request.install_opener(opener)

APPSTORE_URL = "https://www.switchbru.com/appstore/{}"
IMAGE_BASE_URL = APPSTORE_URL.format("packages/{}/{}")
APPSTORE_PACKAGE_URL = "https://www.switchbru.com/appstore/zips/{}.zip"

DOWNLOADSFOLDER = "downloads"

CACHEFOLDER = "cache"
ICON  = "icon.png"
SCREEN = "screen.png"

lib_path = os.path.dirname(os.path.realpath(__file__))
#To blacklist icons
#create a file in the same folder as this on
#Call it icon_blacklist.txt
#Put the package name you'd like to blacklist on it's own line 
blacklist = os.path.join(lib_path, "icon_blacklist.txt")
ICONBLACKLIST = []
if os.path.isdir(blacklist):
    with open(blacklist) as blacklistfile:
        ICONBLACKLIST = blacklistfile.read()
        print("Loaded icon blacklist {}".format(ICONBLACKLIST))

SCREENBUFFER = {}
ICONBUFFER = {}

def download(remote: str, file: str, silent = False):
    try:
        urllib.request.urlretrieve(remote,file)
        return file
    except Exception as e:
        if not silent:
            print(f"failed to download file - {file} from url - {remote}, reason: {e}") 
        return None

#Gets (downloads or grabs from cache) an image of a given type (icon or screenshot) for a given package_name
def getImage(package_name: str, image_type: str, force = False):
    path = os.path.join(os.path.join(sys.path[0], CACHEFOLDER), package_name.replace(":",""))
    if not os.path.isdir(path):
        os.mkdir(path)

    image_file = os.path.join(path, image_type)

    if os.path.isfile(image_file) and not force:
        return(image_file)
    else:
        return download(IMAGE_BASE_URL.format(package_name, image_type), image_file, silent = True)

def getPackageIcon(package_name: str, force = False):
    if not package_name in ICONBLACKLIST:
        if package_name in ICONBUFFER.keys():
            return ICONBUFFER[package_name]
        icon = getImage(package_name, ICON, force = force)
        ICONBUFFER.update({package_name : icon})
        return icon

def getScreenImage(package_name: str, force = False):
    if package_name in SCREENBUFFER.keys():
        return SCREENBUFFER[package_name]
    screen = getImage(package_name, SCREEN, force = force)
    SCREENBUFFER.update({package_name : screen})
    return screen

#Downloads the current zip of a package
def getPackage(package_name: str):
    try:
        downloadsfolder = os.path.join(sys.path[0], DOWNLOADSFOLDER)
        packageURL = APPSTORE_PACKAGE_URL.format(package_name)
        packagefile = os.path.join(downloadsfolder, "{}.zip".format(package_name))
        return download(packageURL, packagefile)
    except Exception as e:
        print(f"Error getting package zip for {package_name} - {e}")