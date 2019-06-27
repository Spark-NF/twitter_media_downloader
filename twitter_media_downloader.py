#!/usr/bin/env python
# coding: utf-8

from __future__ import print_function
import os.path
import io
import sys
import json

# Import local functions
from src.args import parseArgs
from src.parser import getMedias
from src.mapper import generateResults
from src.downloader import download

try: input = raw_input
except NameError: pass


# Parse program arguments
args = parseArgs(sys.argv[1:])
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