#!/usr/bin/env python

from sys import exit
from airos import AirOS
from pprint import pprint
from argparse import ArgumentParser


def main(host=None, username=None, password=None):
    station = AirOS(host=host, username=username, password=password)
    status = station.status
    pprint(status, indent=3)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        action='store',
        dest='host',
        help='The address or hostname of your device.',
    )
    parser.add_argument(
        '-u', '--username',
        action='store',
        default='ubnt',
        dest='username',
        help='The username to access the AirOS status page.',
    )
    parser.add_argument(
        '-p', '--password',
        action='store',
        default='ubnt',
        dest='password',
        help='The password to access the AirOS status page.',
    )

    args = parser.parse_args()
    main(host=args.host, username=args.username, password=args.password)

