WIP lib for interacting with appstore/libget content


##OBJECTS/MODULES:
- appstore_handler - tool for interacting with SD card content
- parser - tool for parsing the appstore team's switch repo
- ext_parser - tool for parsing the appstore team's switch repo, extends parser
- appstore_web - module for accessing appstore content like icons/packages


###appstore_handler (object):
```
Methods:
	set_path(path: str)
		Sets the working path

	check_path()
		Checks if the working path has been set yet

	check_if_get_init()
		Checks if get folder is inited in folder /switch/appstore/ relative to the working oath

	init_get()
		Inits the .get folder if it hasn't been yet

	install_package(repo_entry: dict, silent = False)
		Installs a package, pass it an entry from the appstore repo
	
	uninstall_package(repo_entry: dict)
		Uninstalls a package, pass it an entry from the appstore repo

	remove_store_entry(package_name: str)
		Removes a package entry by deleting the package folder containing the manifest and info.json

	get_package_entry(package_name: str)
		Get the contents of a package's info file as a dict, returns none if it doesn't exist

	get_package_value(package_name: str, key: str)
		Get a value from a package's json file of a given key, returns none if it fails

	get_package_version(package_name: str)
		Get the installed version of a package,returns None if failed

	get_package_manifest(package_name: str)
		Returns a package's manifest as a list

	get_packages(silent = False)
		Returns a list of installed package's package names

	edit_info(package, key, value)
		Edits info json for an installed package

	clean_version(ver, name)
		Returns a cleaned package version, used for comparing versions etc


Attributes:
	appstore_handler.base_install_path 
		#Used internally to store the base path 

	self.packages = none
		Stores a list of discovered installed packages whenever `get_packages` is called
```

###parser (object):
```
Methods:
	clear()
		Clears the object of all loaded data

	load_file(repo_json)
		Loads appstore json file as a large list of dicts

	load_json(repo_json: dict)
		Loads appstore json object as a large list of dicts 

	get_package(packagename: str)
		Returns a package dict given a packages name, returns noe if nothing is found

	def sort(self):
		INTERNAL, sorts packages by category
Attributes:
	parser.all = [] #All homebrew, rest are pretty self-explanatory
	parser.advanced = []
	parser.emus = []
	parser.games = []
	parser.loaders = []
	parser.themes = []
	parser.tools = []
	parser.misc = []
	parser.legacy = []
```

###ext_parser (object):
```
Methods:
	get_package_by_title(self, title: str):
		returns package dict when passed package title, you should avoid using this.

	get_list_of_packages_by_list_of_package_names(self, package_names: list):
		returns a list of package dicts when passed a list of package names

	get_list_of_packages_by_category(self, category: str):
		returns a list of package dicts when passed a category string

	get_list_of_packages_by_list_of_categories(self, categories_list: list):
		returns a list of package dicts when passed a list of category strings

	get_list_of_packages_by_author(self, package_author: str):
		returns a list of package dicts when passed an author string

	get_list_of_packages_by_list_of_authors(self, package_authors: list):
		returns a list of package dicts when passed a list of author strings

	get_packages_list_sorted_by_updated(self, list_reversed: bool = False):
		returns a list of all packages sorted by when they were last updated

	get_packages_list_sorted_by_size(self, list_reversed: bool = False):
		returns a list of all packages sorted by when they were last updated

	get_packages_list_sorted_by_app_dls(self, list_reversed: bool = False):
		returns a list of all packages sorted by app dls

	get_packages_list_sorted_by_web_dls(self, list_reversed: bool = False):
		returns a list of all packages sorted by app dls

	get_list_of_packages_with_binaries(self, packages_list: list = False):
		returns a list of all packages with binaries
```

###appstore_web (module):
```
Functions: 
	getPackageIcon(package_name: str, force = False)
		get package icon for a given package name, force will ignore cached file

	getScreenImage(package_name: str, force = False)
		get screenshot image for a given package name, force will ignore cached file

	getPackage(package_name: str)
		grabs the zip for a package from the appstore team's server
```