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
NEWLINE = '\n'


def get_current_version():
    """
    Get current stable version of WordPress
    """
    r = requests.get(WP_DOWNLOAD_URL)
    match = re.search(
        r'Download&nbsp;WordPress&nbsp;([0-9]+\.[0-9]+\.?[0-9]*)',
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
    # type: (list[str]) -> list[str]
    """
    Check given domains

    :param list domains:
    :return: list of failed domains
    """
    cur_version = get_current_version()
    failed_domains = []

    logging.info('Current stable version is: {}\n'.format(cur_version))

    with concurrent.futures.ThreadPoolExecutor(
        max_workers=MAX_WORKERS
    ) as executor:
        future_to_domain = {
            executor.submit(get_version_installed_on_domain, domain): domain
            for domain in domains
        }

        for future in concurrent.futures.as_completed(future_to_domain):
            domain = future_to_domain[future]

            logging.info('Checking domain {}...'.format(domain))

            try:
                version = future.result()
            except Exception as exc:
                logging.warn('%r generated an exception: %s', domain, exc)
                continue

            if not version:
                logging.warn(
                    ORANGE +
                    'WARN: version not detected'.format(version) +
                    END
                )
                continue

            if version == cur_version:
                logging.info(GREEN + 'OK' + END)
            else:
                logging.warn(
                    RED +
                    'FAIL: version {} detected'.format(version) +
                    END,
                )
                failed_domains.append(domain)

    logging.info(
        NEWLINE +
        ORANGE +
        'Not uptodate domains: {}'.format(', '.join(failed_domains)) +
        END
    )
    return failed_domains


def main():
    if len(sys.argv) < 2:
        print('Usage: {} file_with_domains'.format(sys.argv[0]))
        sys.exit(1)

    logging.root.setLevel(logging.INFO)
    logging.root.handlers = []
    logging.root.addHandler(logging.StreamHandler())
    logging.root.handlers[0].setFormatter(logging.Formatter())

    check_domains(get_domains_from_file(sys.argv[1]))


if __name__ == '__main__':
    main()
