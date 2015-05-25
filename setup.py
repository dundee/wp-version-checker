from setuptools import setup, find_packages
setup(
    name = "wp-version-checker",
    version = "0.0.1",
    packages = find_packages(),
    scripts = ['wp_version_checker.py'],
    author = "Dundee",
    author_email = "daniel@milde.cz",
    description = "Wordpress version checker",
    license = "GPL",
    keywords = "wordpress",
    url = "https://github.com/Dundee/wp-version-checker",
)
