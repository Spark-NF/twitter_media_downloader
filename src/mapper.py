# coding: utf-8

import json
import re
from os.path import splitext, basename

try:
    from urllib.parse import urlparse
except ImportError:
     from urlparse import urlparse


def slugify(value):
	import unicodedata
	value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
	value = re.sub('[<>/\\:"|?*]', '-', value).strip().lower()
	return value

def parseFilename(format, tweetId, originalTweetId, date, originalDate, url):
	disassembled = urlparse(url)
	file = basename(disassembled.path)
	file = re.sub(':(?:thumb|small|medium|large)$', '', file)
	filename, ext = splitext(file)
	replaced = format.replace('%date%', date) \
		.replace('%original_date%', originalDate) \
		.replace('%tweet_id%', tweetId) \
		.replace('%original_tweet_id%', originalTweetId) \
		.replace('%filename%', filename) \
		.replace('%ext%', ext[1:])
	slugified = slugify(replaced)
	return slugified

def generateResults(inputFile, outputFile, filenameFormat):
	file = open(inputFile).read()
	data = json.loads(file)

	results = {
		'files': {},
		'urls': {
			'periscope': [],
			'instagram': [],
			'others': []
		},
		'text': []
	}

	for media in data['media']:
		# Text
		if media['text']:
			results['text'].append(media['text'])

		# Urls
		for urlType in media['urls']:
			for url in media['urls'][urlType]:
				results['urls'][urlType].append(url)

		# Files
		for url in media['images'] + media['videos']:
			filename = parseFilename(filenameFormat, media['tweet_id'], media['original_tweet_id'], media['date'], media['original_date'], url)
			results['files'][filename] = url

	with open(outputFile, 'w') as file:
		json.dump(results, file, indent=4, default=lambda x:str(x))