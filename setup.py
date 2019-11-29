import re
import subprocess

from setuptools import setup, find_packages

DEFAULT_VERSION = "0.0.0"
AUTHOR = 'ChihYing_Lin'
EMAIL = ''
PACKAGE_NAME = 'cy_rwlock'
URL = 'https://github.com/cy-arduino/' + PACKAGE_NAME
LICENSE = 'LGPL'
DESCRIPTION = ''


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


try:
    version = subprocess.check_output(
        'git describe --tags', shell=True).rstrip().decode('utf-8')
except subprocess.CalledProcessError:
    version = DEFAULT_VERSION

setup(name=PACKAGE_NAME,
      version=version,
      description=DESCRIPTION,
      url=URL,
      author=AUTHOR,
      author_email=EMAIL,
      license=LICENSE,
      packages=find_packages(exclude=['tests', 'test_*']),
      zip_safe=False)
