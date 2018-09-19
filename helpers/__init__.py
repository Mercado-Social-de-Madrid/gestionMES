__all__ = ['decorators', 'fcm', 'filesystem', 'query', 'mailing']

import pip

def is_package_installed(package_name):
    installed_packages = pip.get_installed_distributions()
    packages = [package.project_name for package in installed_packages]
    return package_name in packages

from decorators import *
from fcm import *
from filesystem import *
from query import *
from mailing import *

