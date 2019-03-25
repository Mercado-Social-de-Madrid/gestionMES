__all__ = ['decorators', 'fcm', 'filesystem', 'query', 'mailing']

import pip

def is_package_installed(package_name):
    if hasattr(pip, 'get_installed_distributions'):
        loader = pip.get_installed_distributions
    else:
        loader = pip._internal.utils.misc.get_installed_distributions

    installed_packages = loader()
    packages = [package.project_name for package in installed_packages]
    return package_name in packages

from decorators import *
from fcm import *
from filesystem import *
from query import *
from mailing import *

