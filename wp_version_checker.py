#!/usr/bin/env python
import sys
import urllib.request
import urllib.error
import re
import logging

WP_DOWNLOAD_URL = 'https://wordpress.org/download/'

GREEN = '\033[92m'
RED = '\033[91m'
ORANGE = '\033[93m'
END = '\033[0m'


def get_current_version():
    with urllib.request.urlopen(WP_DOWNLOAD_URL) as fp:
        match = re.search(r'Download&nbsp;WordPress&nbsp;([0-9]+\.[0-9]+\.[0-9]+)', str(fp.read()))
        if match:
            return match.group(1)
        else:
            raise Exception('Cannot read current stable WP version')


def get_version_installed_on_domain(domain):
    try:
        with urllib.request.urlopen('http://{}/readme.html'.format(domain)) as fp:
            match = re.search(r'Version ([0-9]+\.[0-9]+\.[0-9]+)', str(fp.read()))
            if match:
                return match.group(1)
            else:
                logging.warning('Cannot read WP version of domain {}'.format(domain))
    except (urllib.error.HTTPError, urllib.error.URLError):
        logging.warning('Cannot read WP version of domain {}'.format(domain))


def get_domains_from_file(domains_file):
    with open(domains_file, 'r') as fp:
        for line in fp:
            yield line.strip()


def check_domains(domains):
    cur_version = get_current_version()
    failed_domains = []

    print('Current stable version is: {}'.format(cur_version))
    print()

    for domain in domains:
        print('Checking domain {}...'.format(domain), end='')

        version = get_version_installed_on_domain(domain)

        if not version:
            print(ORANGE, 'WARN: version not detected'.format(version), END, sep='')
            continue

        if version == cur_version:
            print(GREEN, 'OK', END, sep='')
        else:
            print(RED, 'FAIL: version {} detected'.format(version), END, sep='')
            failed_domains.append(domain)

    print()
    print(ORANGE, 'Not uptodate domains: {}'.format(', '.join(failed_domains)), END, sep='')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: {} file_with_domains'.format(sys.argv[0]))
        sys.exit(1)

    domains = get_domains_from_file(sys.argv[1])
    check_domains(domains)
