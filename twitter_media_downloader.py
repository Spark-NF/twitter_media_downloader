#!/usr/bin/env python
# coding: utf-8

from __future__ import print_function
import argparse
from datetime import datetime
import os.path
import io
import sys
import json

# Import local functions
from src.parser import getMedias
from src.mapper import generateResults
from src.downloader import download

try: input = raw_input
except NameError: pass


# Datetime parser for argparse
def valid_date(s):
	try:
		return datetime.strptime(s, "%Y-%m-%d %H:%M")
	except ValueError:
		try:
			return datetime.strptime(s, "%Y-%m-%d")
		except ValueError:
			msg = "Not a valid date: '{0}'.".format(s)
			raise argparse.ArgumentTypeError(msg)

# Setup argparse
parser = argparse.ArgumentParser(description='Twitter media downloader.')
parser.add_argument('userid', type=str, help='the account name or ID')
parser.add_argument('-o', '--output', type=str, metavar='DIR', help='the output directory', default='out')
parser.add_argument('-f', '--format', type=str, metavar='FORMAT', help='the filename format', default='[%date%] %filename%.%ext%')
parser.add_argument('-s', '--image-size', type=str, metavar='IMAGE_SIZE', help='the preferred image size to download', default='medium', choices=['thumb', 'small', 'medium', 'large'])
parser.add_argument('--since', type=valid_date, metavar='DATE', help='the start date of the search')
parser.add_argument('--since-id', type=int, metavar='ID', help='the start ID of the search')
parser.add_argument('--until', type=valid_date, metavar='DATE', help='the end date of the search')
parser.add_argument('--until-id', type=int, metavar='ID', help='the end ID of the search')
parser.add_argument('-r', '--retweets', help='also download medias from retweets', action='store_true')
parser.add_argument('-u', '--userid', help='append userid to output directory', action='store_true', dest='o_userid')
parser.add_argument('-q', '--quiet', help='disable output', action='store_true')

# Get argparse result
args = parser.parse_args()
userId = args.userid
outputDir = os.path.join(args.output, userId + os.sep if args.o_userid else '')
filenameFormat = args.format
since = args.since
sinceId = args.since_id
until = args.until
untilId = args.until_id
includeRetweets = args.retweets
imageSize = args.image_size
quiet = args.quiet


# Twitter OAuth
oauthFile = '.oauth.json'
if not os.path.exists(oauthFile):
	auth = {
		'consumer_token': '',
		'consumer_secret': ''
	}
	auth['consumer_token'] = input('Token: ')
	auth['consumer_secret'] = input('Secret: ')

	with open(oauthFile, 'w') as file:
		json.dump(auth, file, indent=4, default=lambda x:str(x))
else:
	file = open(oauthFile).read()
	auth = json.loads(file)


# Create output directory if necessary
if not os.path.exists(outputDir):
	os.makedirs(outputDir)


if quiet:
	sys.stdout = open(os.devnull, 'w')

medias = getMedias(auth, userId, includeRetweets, imageSize, since, sinceId, until, untilId)
results = generateResults(medias, filenameFormat)
download(results, outputDir, False, False)