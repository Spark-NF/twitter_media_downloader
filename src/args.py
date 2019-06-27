# coding: utf-8

import argparse
from datetime import datetime


# Datetime parser for argparse
def parseDate(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d %H:%M")
    except ValueError:
        try:
            return datetime.strptime(s, "%Y-%m-%d")
        except ValueError:
            msg = "Not a valid date: '{0}'.".format(s)
            raise argparse.ArgumentTypeError(msg)

def parseArgs(args):
    parser = argparse.ArgumentParser(description='Twitter media downloader.')
    parser.add_argument('userid', type=str, help='the account name or ID')
    parser.add_argument('-o', '--output', type=str, metavar='DIR', help='the output directory', default='out')
    parser.add_argument('-f', '--format', type=str, metavar='FORMAT', help='the filename format', default='[%date%] %filename%.%ext%')
    parser.add_argument('-s', '--image-size', type=str, metavar='IMAGE_SIZE', help='the preferred image size to download', default='medium', choices=['thumb', 'small', 'medium', 'large'])
    parser.add_argument('--since', type=parseDate, metavar='DATE', help='the start date of the search')
    parser.add_argument('--since-id', type=int, metavar='ID', help='the start ID of the search')
    parser.add_argument('--until', type=parseDate, metavar='DATE', help='the end date of the search')
    parser.add_argument('--until-id', type=int, metavar='ID', help='the end ID of the search')
    parser.add_argument('-r', '--retweets', help='also download medias from retweets', action='store_true')
    parser.add_argument('-u', '--userid', help='append userid to output directory', action='store_true', dest='o_userid')
    parser.add_argument('-q', '--quiet', help='disable output', action='store_true')
    return parser.parse_args(args)