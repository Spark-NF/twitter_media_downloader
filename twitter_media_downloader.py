#!/usr/bin/env python

from __future__ import print_function
import argparse
import os.path
import io
import sys
import json
from parser import getMedias
from mapper import generateResults
from downloader import download

try: input = raw_input
except NameError: pass


# Setup argparse
parser = argparse.ArgumentParser(description='Twitter media downloader.')
parser.add_argument('userid', type=str, help='the account name or ID')
parser.add_argument('-o', '--output', type=str, metavar='DIR', help='the output directory', default='out')
parser.add_argument('-f', '--format', type=str, metavar='FORMAT', help='the filename format', default='[%date%] %filename%.%ext%')
parser.add_argument('-u', '--userid', help='append userid to output directory', action='store_true', dest='o_userid')
parser.add_argument('-q', '--quiet', help='disable output', action='store_true')

# Get argparse result
args = parser.parse_args()
userId = args.userid
outputDir = os.path.join(args.output, userId + os.sep if args.o_userid else '')
filenameFormat = args.format
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


# Create output and tmp directory if necessary
if not os.path.exists('tmp'):
	os.makedirs('tmp')
if not os.path.exists(outputDir):
	os.makedirs(outputDir)


urlsFile = 'tmp/' + userId + '_urls.json'
downloadsFile = 'tmp/' + userId + '_download.json'

if quiet:
	sys.stdout = open(os.devnull, 'w')

getMedias(auth, userId, urlsFile)
generateResults(urlsFile, downloadsFile, filenameFormat)
download(downloadsFile, outputDir, False, False)