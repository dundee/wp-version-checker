# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    read_md = lambda f: open(f, 'r').read()

setup(
    name = "wp-version-checker",
    version = "0.1.3",
    packages = find_packages(),
    scripts = ['wp_version_checker.py'],
    author = "Dundee",
    author_email = "daniel@milde.cz",
    description = "Wordpress version checker",
    license = "GPL",
    keywords = "wordpress",
    url = "https://github.com/Dundee/wp-version-checker",
    long_description = read_md('README.md'),
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.4",
    ]
)
