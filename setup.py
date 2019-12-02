import re
import os
import subprocess

from setuptools import setup, find_packages

##########################################################
DEFAULT_VERSION = "0.0.0"
AUTHOR = 'ChihYing_Lin'
EMAIL = ''
PACKAGE_NAME = 'cy_rwlock'
URL = 'https://github.com/cy-arduino/' + PACKAGE_NAME
LICENSE = 'LGPL'
DESCRIPTION = 'RwLock: Reader-Writer lock'
LONG_DESCRIPTION_FILE = 'README.md'
LONG_DESCRIPTION_TYPE = 'text/markdown'
##########################################################


# convert version from git tag to pypi style
# V0.1-3-g908f162 -> V0.1.post3
def convert_version(git_version):
    print("ori version: {}".format(git_version))

    pattern = re.compile(
        r"^[vV]*(?P<main>[0-9.]+)(-(?P<post>[0-9]+))?(-.+)?$")
    ver = pattern.search(git_version)

    if not ver:
        print("invalid version! return default version {}".format(
            DEFAULT_VERSION))
        return DEFAULT_VERSION

    new_ver = ver.group('main')

    if ver.group('post'):
        new_ver += ".post{}".format(ver.group('post'))

    print("new version: {}".format(new_ver))
    return new_ver


def get_pypi_version():
    try:
        version = subprocess.check_output(
            'git describe --tags', shell=True).rstrip().decode('utf-8')
        version = convert_version(version)
    except subprocess.CalledProcessError:
        version = DEFAULT_VERSION

    return version


def read_file(file_name):
    # noinspection PyBroadException
    try:
        cur_path = os.path.abspath(os.path.dirname(__file__))
        with open(os.path.join(cur_path, file_name)) as f:
            long_description = f.read()
    except Exception:
        long_description = ""
    return long_description


setup(name=PACKAGE_NAME,
      version=get_pypi_version(),
      description=DESCRIPTION,
      url=URL,
      author=AUTHOR,
      author_email=EMAIL,
      license=LICENSE,
      packages=find_packages(exclude=['tests', 'test_*']),
      long_description=read_file(LONG_DESCRIPTION_FILE),
      long_description_content_type=LONG_DESCRIPTION_TYPE,
      zip_safe=False)
