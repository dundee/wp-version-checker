#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script for checking if version of WordPress sites is up-to-date

Usage: wp_version_checker.py file_with_domains
"""

from __future__ import print_function

import sys
import requests
import re
import logging
import concurrent.futures

WP_DOWNLOAD_URL = 'https://wordpress.org/download/'
MAX_WORKERS = 5

GREEN = '\033[92m'
RED = '\033[91m'
ORANGE = '\033[93m'
END = '\033[0m'


def get_current_version():
    """
    Get current stable version of WordPress
    """
    r = requests.get(WP_DOWNLOAD_URL)
    match = re.search(
        r'Download&nbsp;WordPress&nbsp;([0-9]+\.[0-9]+\.?[0-9]+)',
        str(r.text)
    )
    if match:
        return match.group(1)
    else:
        raise Exception('Cannot read current stable WP version')


def get_version_installed_on_domain(domain):
    """
    Get WordPress version installed on given domain

    :param str domain:
    """
    try:
        r = requests.get('http://{}/readme.html'.format(domain))
        match = re.search(
            r'Version ([0-9]+\.[0-9]+\.?[0-9]*)',
            str(r.text)
        )
        if match:
            return match.group(1)
        else:
            logging.warning(
                'Cannot read WP version of domain {}'.format(domain)
            )
    except requests.exceptions.HTTPError:
        logging.warning(
            'Cannot read WP version of domain {}'.format(domain)
        )


def get_domains_from_file(domains_file):
    """
    Get list of domains from file

    :param str domains_file: path to file with domains
    :return: list
    """
    with open(domains_file, 'r') as opened_file:
        for line in opened_file:
            yield line.strip()


def check_domains(domains):
    """
    Check given domains

    :param list domains:
    """
    cur_version = get_current_version()
    failed_domains = []

    print('Current stable version is: {}'.format(cur_version))
    print()

    with concurrent.futures.ThreadPoolExecutor(
        max_workers=MAX_WORKERS
    ) as executor:
        future_to_domain = {
            executor.submit(get_version_installed_on_domain, domain): domain
            for domain in domains
        }

        for future in concurrent.futures.as_completed(future_to_domain):
            domain = future_to_domain[future]

            print('Checking domain {}...'.format(domain), end='')

            try:
                version = future.result()
            except Exception as exc:
                print('%r generated an exception: %s' % (domain, exc))
                continue

            if not version:
                print(
                    ORANGE,
                    'WARN: version not detected'.format(version),
                    END,
                    sep=''
                )
                continue

            if version == cur_version:
                print(GREEN, 'OK', END, sep='')
            else:
                print(
                    RED,
                    'FAIL: version {} detected'.format(version),
                    END,
                    sep=''
                )
                failed_domains.append(domain)

    print()
    print(
        ORANGE,
        'Not uptodate domains: {}'.format(', '.join(failed_domains)),
        END,
        sep=''
    )


def main():
    if len(sys.argv) < 2:
        print('Usage: {} file_with_domains'.format(sys.argv[0]))
        sys.exit(1)

    check_domains(get_domains_from_file(sys.argv[1]))


if __name__ == '__main__':
    main()
