#!/usr/bin/env python
# coding: utf-8

import os.path
import sys

# Import local functions
from src.args import parseArgs
from src.config import getOAuth
from src.parser import getMedias
from src.mapper import generateResults
from src.downloader import download


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
auth = getOAuth('.oauth.json')


# Create output directory if necessary
if not os.path.exists(outputDir):
    os.makedirs(outputDir)


if quiet:
    sys.stdout = open(os.devnull, 'w')

medias = getMedias(auth, userId, includeRetweets, imageSize, since, sinceId, until, untilId)
results = generateResults(medias, filenameFormat)
download(results, outputDir, False, False)
