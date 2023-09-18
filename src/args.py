# coding: utf-8

"""
CLI arguments parser.
"""

import argparse
from datetime import datetime


def parse_date(date):
    """Datetime parser for argparse."""
    try:
        return datetime.strptime(date, "%Y-%m-%d %H:%M")
    except ValueError:
        try:
            return datetime.strptime(date, "%Y-%m-%d")
        except ValueError as exc:
            msg = f"Not a valid date: '{date}'."
            raise argparse.ArgumentTypeError(msg) from exc


def parse_args(args):
    """Parse the arguments passed to twitter_media_downloader using argparse."""
    parser = argparse.ArgumentParser(description='Twitter media downloader.')
    parser.add_argument('userid', type=str, nargs='+', help='the account name or ID, prefix with @ to open as file (one account per line)')
    parser.add_argument('-o', '--output', type=str, metavar='DIR', help='the output directory', default='out')
    parser.add_argument('-f', '--format', type=str, metavar='FORMAT', help='the filename format', default='[%date%] %filename%.%ext%')
    parser.add_argument('-s', '--image-size', type=str, metavar='IMAGE_SIZE', help='the preferred image size to download', default='medium', choices=['thumb', 'small', 'medium', 'large', 'orig'])
    parser.add_argument('--since', type=parse_date, metavar='DATE', help='the start date of the search')
    parser.add_argument('--since-id', type=int, metavar='ID', help='the start ID of the search')
    parser.add_argument('--until', type=parse_date, metavar='DATE', help='the end date of the search')
    parser.add_argument('--until-id', type=int, metavar='ID', help='the end ID of the search')
    parser.add_argument('-r', '--retweets', help='also download medias from retweets', action='store_true')
    parser.add_argument('-l', '--likes', help='download user liked medias', action='store_true')
    parser.add_argument('-u', '--userid', help='append userid to output directory', action='store_true', dest='o_userid')
    parser.add_argument('-q', '--quiet', help='disable output', action='store_true')
    return parser.parse_args(args)


def parse_file_arg(arg):
    """Handles @file format for users, to load the list of users from said file, one per line."""
    if not isinstance(arg, list):
        arg = [arg]
    ret = []
    for val in arg:
        if val[0] == '@':
            with open(val[1:], encoding='utf-8') as arg_file:
                ret.extend(arg_file.readlines())
        else:
            ret.append(val)
    return [x.strip() for x in ret if x.strip() != '']
