# Some basic scripts for installing appstore zips given the package name
# Loosely based on vgmoose's libget here: https://github.com/vgmoose/libget
# Copyright LyfeOnEdge 2019
# Licensed under GPL3

import sys
import os
import shutil
import json
from zipfile import ZipFile
from .appstore_web import getPackage

# Standard path to find the appstore at
PACKAGES_DIR = "switch/appstore/.get/packages"
# Name of package info file
PACKAGE_INFO = "info.json"
# Name of pagkade manifest file
PACKAGE_MANIFEST = "manifest.install"
# The prefix used to designate each line in the manifest
MANIFEST_PREFIX = "U: "


class appstore_handler(object):
    def __init__(self):
        self.base_install_path = None
        self.packages = None

    # Check if the appstore packages folder has been inited
    def check_if_get_init(self):
        if not self.check_path():
            return warn_path_not_set()
        # Append package name to packages directory
        packagesdir = os.path.join(self.base_install_path, PACKAGES_DIR)
        try:
            return os.path.isdir(packagesdir)
        except:
            pass

    def init_get(self):
        if not self.check_path():
            return warn_path_not_set()
        if not self.check_if_get_init():
            packagesdir = os.path.join(self.base_install_path, PACKAGES_DIR)
            os.makedirs(packagesdir)
            return True
        else:
            print("Appstore packages dir already inited")

    # Set this to a root of an sd card or in a dir to test
    def set_path(self, path: str):
        self.base_install_path = path
        print(f"Set SD Root path to {path}")
        self.packages = None
        self.get_packages()

    def reload(self):
        self.set_path(self.base_install_path)

    def check_path(self):
        return self.base_install_path


    # Installs an appstore package
    def install_package(self, package: dict, silent=False):
        if not self.check_path():
            return warn_path_not_set()

        if not package:
            print("No repo entry data passed to appstore handler.")
            print("Not continuing with install")
            return
        try:
            package_name = package["name"]
        except:
            print("Error - package name not found in repo data")
            print("Not continuing with install")
            return

        try:
            version = package["version"]
        except:
            print("Error - package version not found in repo data")
            print("Not continuing with install")
            return

        title = f"Installing {package_name}"
        if version:
            title += f" - {version}"

        if not self.check_if_get_init():
            print("Get folder not initiated.")
            print("Not continuing with install")
            return

        # Uninstall if already installed
        if package_name in self.get_packages(silent=True):
            print("Package already installed, removing for upgrade")
            if not self.uninstall_package(package):
                # If uninstall fails
                print("Uninstall failed.")
                print("Not continuing with install")
                return

        else:
            print("Package not previously installed, proceeding...")

        print(f"Beginning install for package {package_name}")

        # Append base directory to packages directory
        packagesdir = os.path.join(self.base_install_path, PACKAGES_DIR)
        if not os.path.isdir(packagesdir):
            os.makedirs(packagesdir)
        # Append package folder to packages directory
        packagedir = os.path.join(packagesdir, package_name)
        if not os.path.isdir(packagedir):
            os.mkdir(packagedir)

        # Download the package from the switchbru site
        appstore_zip = getPackage(package_name)
        if not appstore_zip:
            print(f"Failed to download zip for package {package_name}")
            return

        with ZipFile(appstore_zip) as zipObj:
            namelist = zipObj.namelist()
            # Easy check to see if info and manifest files are in the zip
            if not PACKAGE_MANIFEST in namelist:
                print(
                    "Failed to find package manifest in zip... Stopping install, no files have been changed on the SD card")
                return
            if not PACKAGE_INFO in namelist:
                print(
                    "Failed to find package info in zip... Stopping install, no files have been changed on the SD card")
                return

            # Extract everything but the manifest and the info file
            extract_manifest = []
            for filename in zipObj.namelist():
                if filename == PACKAGE_MANIFEST or filename == PACKAGE_INFO:
                    pass
                else:
                    zipObj.extract(filename, path=self.base_install_path)
                    extract_manifest.append(filename)

            print("Extracted: {}".format(json.dumps(extract_manifest, indent=4)))

            # Extract manifest
            zipObj.extract(PACKAGE_MANIFEST, path=packagedir)
            print("Wrote package manifest.")

            # Extract info file
            zipObj.extract(PACKAGE_INFO, path=packagedir)
            print("Wrote package info.")

        os.remove(appstore_zip)

        print("Installed {} version {}".format(package["title"], version))

        self.reload()


    # Uninstalls a package given a chunk from the repo
    def uninstall_package(self, package: dict):
        if not self.check_path():
            return warn_path_not_set()
        if not package:
            print("No repo entry data passed to appstore handler.")
            print("Not continuing with uninstall")
            return
        if not self.check_if_get_init():
            print("Appstore get folder not initiated.")
            print("Not continuing with uninstall")
            return

        package_name = package["name"]
        print(f"Uninstalling {package_name}")
        if not self.get_package_entry(package_name):
            print("Could not find package in currently selected location.")
            print("Not continuing with uninstall")
            return

        filestoremove = self.get_package_manifest(package_name)
        if 'str' in str(type(filestoremove)):
            file = os.path.join(self.base_install_path, filestoremove)
            if os.path.isfile(file):
                os.remove(file)
                print(f"removed {file}")
        else:
            # Go through the previous ziplist in reverse, this way folders get
            # cleaned up
            for path in reversed(filestoremove):
                file = os.path.join(self.base_install_path, path)
                if os.path.isfile(file):
                    os.remove(file)
                    print(f"removed {file}")
                elif os.path.isdir(file):
                    if not os.listdir(file):
                        os.rmdir(file)
                        print(f"removed empty directory {file}")

        self.remove_store_entry(package_name)

        print(f"Uninstalled package {package_name}")

        self.reload()
        return True


    # THIS DOES NOT UNINSTALL THE CONTENT
    # Removes a package entry by deleting the package
    # folder containing the manifest and info.json
    def remove_store_entry(self, package_name: str):
        if not self.check_path():
            return warn_path_not_set()
        # Append package name to packages directory
        pacdir = os.path.join(PACKAGES_DIR, package_name)
        # Append base directory to packages directory
        packagedir = os.path.join(self.base_install_path, pacdir)
        try:
            shutil.rmtree(packagedir, ignore_errors=True)
            print(f"Removed appstore entry for {package_name}")
        except Exception as e:
            print(f"Error removing store entry for {package_name} - {e}")


    # Get the contents of a package's info file as a dict
    # Returns none if it doesn't exist
    def get_package_entry(self, package_name: str):
        if not self.check_path():
            return
        # Append package name to packages directory
        pacdir = os.path.join(PACKAGES_DIR, package_name)
        # Append base directory to packages directory
        packagedir = os.path.join(self.base_install_path, pacdir)
        # Append package loc to info file name
        pkg = os.path.join(packagedir, PACKAGE_INFO)

        try:
            with open(pkg, encoding="utf-8") as infojson:
                return json.load(infojson)
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Failed to open repo_entry data for {package_name} - {e}")


    # Get a package's json file value, returns none if it fails
    def get_package_value(self, package_name: str, key: str):
        if not self.check_path():
            return
        # Get the package json data
        package_info = self.get_package_entry(package_name)
        # If data was retrieved, return the value
        if package_info:
            return package_info[key]


    # Get the installed version of a package
    def get_package_version(self, package_name: str):
        return self.get_package_value(package_name, "version")


    # Returns a package's manifest as a list
    def get_package_manifest(self, package_name: str):
        if not self.check_path():
            return warn_path_not_set()
        # Append package name to packages directory
        pacdir = os.path.join(PACKAGES_DIR, package_name)
        # Append base directory to packages directory
        packagedir = os.path.join(self.base_install_path, pacdir)
        # Append package loc to manifest file name
        manifestfile = os.path.join(packagedir, PACKAGE_MANIFEST)
        print(manifestfile)
        if not os.path.isfile(manifestfile):
            print("couldn't find manifest")
            return

        mf = []
        # open the manifest, append the current base path to each line
        with open(manifestfile, "r") as maf:
            for fileline in maf:
                fl = fileline.replace(MANIFEST_PREFIX, "")
                fl = fl.strip().replace("\n", "")
                mf.append(os.path.join(self.base_install_path, fl))

        return mf


    def get_packages(self, silent=False):
        if not self.check_path():
            return warn_path_not_set()
        packagedir = os.path.join(self.base_install_path, PACKAGES_DIR)

        if os.path.isdir(packagedir):
            packages_dir_items = os.listdir(packagedir)

            packages = []
            # Go through items in packages dir
            for possible_package in packages_dir_items:
                # Find the path of the package
                pathed_package = os.path.join(packagedir, possible_package)
                package_json = os.path.join(pathed_package, PACKAGE_INFO)
                # check if the json exists (isfile will result in exception if
                # it doesn't exist, it's unlikely to find a folder named
                # info.json, either way exists() will have to be called)
                if os.path.exists(package_json):
                    packages.append(possible_package)
            self.packages = packages
            if not silent:
                print("Found packages -\n{}".format(json.dumps(packages, indent=4)))
            return packages


    def edit_info(self, package_name: str, key: str, value):
        if not self.check_path():
            return warn_path_not_set()
        packagedir = os.path.join(self.base_install_path, PACKAGES_DIR)
        packagesdir = os.path.join(self.base_install_path, PACKAGES_DIR)
        packagedir = os.path.join(packagesdir, package_name)
        pkg = os.path.join(packagedir, PACKAGE_INFO)

        try:
            with open(pkg, encoding="utf-8") as infojson:
                info = json.load(infojson)
        except Exception as e:
            print(f"Failed to open info data for {package_name} - {e}")
            return

        info[key] = value

        with open(pkg, "w", encoding="utf-8") as infojson:
            json.dump(info, infojson)

        return True


    def clean_version(self, ver, name):
        ver = ver.lower().strip("v")
        if name:
            ver = ver.replace(name.lower(), "")
        ver = ver.split(" ")[0].replace("switch", "").strip("-")
        return ver


def warn_path_not_set():
    print("Warning: appstore path not set")
