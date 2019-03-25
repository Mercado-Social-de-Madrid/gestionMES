__all__ = ['decorators', 'fcm', 'filesystem', 'query', 'mailing']

import pkg_resources

def is_package_installed(package_name):

    installed_packages = pkg_resources.working_set
    packages = [package.project_name for package in installed_packages]
    return package_name in packages

from decorators import *
from fcm import *
from filesystem import *
from query import *
from mailing import *

