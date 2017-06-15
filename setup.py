# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import sys

try:
    long_description = open("README.rst").read()
except IOError:
    long_description = ""

PY2 = sys.version_info[0] == 2

requires = ['requests']

if PY2:
    requires.append('futures')

setup(
    name="wp-version-checker",
    version="0.4.1",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'wp-version-checker=wp_version_checker:main',
        ]
    },
    py_modules=['wp_version_checker'],
    author="Dundee",
    author_email="daniel@milde.cz",
    description="Wordpress version checker",
    license="GPL",
    keywords="wordpress",
    url="https://github.com/Dundee/wp-version-checker",
    long_description=long_description,
    install_requires=requires,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Development Status :: 5 - Production/Stable",
        "Topic :: Internet :: WWW/HTTP :: Site Management",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
    ]
)
