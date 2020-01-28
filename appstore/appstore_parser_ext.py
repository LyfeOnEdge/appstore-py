from .appstore_parser import parser

from datetime import datetime

class ext_parser(parser):
	def __init__(self):
		super().__init__()

	#Only really useful if there is only one matching item
	def _get_package_by_field_and_key(self, field: str, key: str):
		if self.all:
			for package in self.all:
				if package[field] == key:
					return package

	def _get_list_of_packages_by_field_and_key(self, field: str, key: str):
		if self.all:
			packages = []
			for package in self.all:
				if package[field] == key:
					packages.append(package)
			return packages

	def get_package_by_title(self, title: str): #This is bad practice but :shrug:
		return self._get_package_by_field_and_key("title", title)

	def get_list_of_packages_by_list_of_package_names(self, package_names: list):
		return [self.get_package(package_name) for package_name in package_names]

	def get_list_of_packages_by_category(self, category: str):
		return self._get_list_of_packages_by_field_and_key("category", category)

	def get_list_of_packages_by_list_of_categories(self, categories_list: list):
		packages = []
		for category in categories_list:
			packages.extend(self._get_list_of_packages_by_field_and_key("category", category))	
		return packages

	def get_list_of_packages_by_author(self, package_author: str):
		return self._get_list_of_packages_by_field_and_key("author", package_author)

	def get_list_of_packages_by_list_of_authors(self, package_authors: list):
		packages = []
		for author in package_authors:
			packages.extend(self._get_list_of_packages_by_field_and_key("author", author))	
		return packages

	def get_packages_list_sorted_by_updated(self, list_reversed: bool = False):
		pkgs = sorted(self.all, key=lambda x: datetime.strptime(x['updated'], '%d/%m/%Y'))
		return pkgs if not list_reversed else [pkg for pkg in reversed(pkgs)]

	def _sort_packages_by_field(self, field: str, list_reversed: bool = False):
		pkgs = sorted(self.all, key=lambda x: x[field])
		return pkgs if not list_reversed else [pkg for pkg in reversed(pkgs)]

	def get_packages_list_sorted_by_size(self, list_reversed: bool = False):
		return self._sort_packages_by_field("extracted", list_reversed)

	def get_packages_list_sorted_by_app_dls(self, list_reversed: bool = False):
		return self._sort_packages_by_field("app_dls", list_reversed)

	def get_packages_list_sorted_by_web_dls(self, list_reversed: bool = False):
		return self._sort_packages_by_field("app_dls", list_reversed)

	def get_list_of_packages_with_binaries(self, packages_list: list = False):
		if (packages_list or self.all):
			packages = []
			for package in (packages_list or self.all):
				if not package["binary"] in ["none", "n/a"]:
					packages.append(package)
			return packages

