Wordpress version checker
=========================

Script for checking version of Wordpress sites

Usage:

::

    wp-version-checker file_with_domains

Output:

::

    Current stable version is: 4.2.2

    Checking domain example.com...OK
    Checking domain xxx.com...FAIL: version 4.1.5 detected
    Checking domain some.org...WARN: version not detected

    Not uptodate domains: xxx.com


