# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import sys

try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    read_md = lambda f: open(f, 'r').read()

PY2 = sys.version_info[0] == 2

requires = ['requests']

if PY2:
    requires.append('futures')

setup(
    name="wp-version-checker",
    version="0.2.0",
    packages=find_packages(),
    scripts=['wp_version_checker.py'],
    author="Dundee",
    author_email="daniel@milde.cz",
    description="Wordpress version checker",
    license="GPL",
    keywords="wordpress",
    url="https://github.com/Dundee/wp-version-checker",
    long_description=read_md('README.md'),
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
