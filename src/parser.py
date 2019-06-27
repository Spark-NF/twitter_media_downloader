# coding: utf-8

from __future__ import print_function
import tweepy
import json
import os
from .medias import VideoMedia


def parseTweet(tweet, includeRetweets, imageSize, results):
	urls = {
		'tweet_id': tweet.id_str,
		'original_tweet_id': tweet.id_str,
		'date': tweet.created_at,
		'original_date': tweet.created_at,
		'videos': [],
		'images': [],
		'urls': {
			'periscope': [],
			'instagram': [],
			'others': []
		},
		'text': '' # tweet.full_text
	}

	if includeRetweets and hasattr(tweet, 'retweeted_status'):
		tweet = tweet.retweeted_status
		urls['original_tweet_id'] = tweet.id_str
		urls['original_date'] = tweet.created_at
		results['retweets'] += 1
	else:
		results['tweets'] += 1

	if hasattr(tweet, 'extended_entities'):
		if 'media' in tweet.extended_entities:
			for media in tweet.extended_entities['media']:
				# Videos
				if 'video_info' in media:
					variants = media['video_info']['variants']
					video = max(VideoMedia(variant) for variant in variants)
					urls['videos'].append(video.obj['url'])

				# Images
				if 'sizes' in media:
					url = media['media_url_https']
					if imageSize in media['sizes']:
						url += ":" + imageSize
					urls['images'].append(url)

	# Urls
	if hasattr(tweet, 'entities'):
		if 'urls' in tweet.entities:
			for url in tweet.entities['urls']:
				expanded = url['expanded_url']
				if 'instagram.com' in expanded:
					urls['urls']['instagram'].append(expanded)
				elif 'periscope.tv' in expanded:
					urls['urls']['periscope'].append(expanded)
				else:
					urls['urls']['others'].append(expanded)

	# Remove thumbnails
	if len(urls['videos']) == 1 and len(urls['images']) and 'video_thumb' in urls['images'][0]:
		urls['images'] = urls['images'][1:]

	if len(urls['videos']) == 0 and len(urls['images']) == 0 and len(urls['urls']['periscope']) == 0 and len(urls['urls']['instagram']) == 0 and hasattr(tweet, 'full_text'):
		urls['text'] = tweet.full_text

	results['media'].append(urls)

def getMedias(auth, userId, includeRetweets, imageSize, outputFile, since, sinceId, until, untilId):
	auth = tweepy.OAuthHandler(auth['consumer_token'], auth['consumer_secret'])
	api = tweepy.API(auth)

	results = {
		'tweets': 0,
		'retweets': 0,
		'media': []
	}
	for tweet in tweepy.Cursor(api.user_timeline, id=userId, include_rts=includeRetweets, include_entities=True, tweet_mode='extended', since_id=sinceId, max_id=untilId).items():
		if since is not None and tweet.created_at < since:
			break
		if until is not None and tweet.created_at > until:
			continue
		parseTweet(tweet, includeRetweets, imageSize, results)

	print('Tweets: {0}'.format(results['tweets']))
	print('Retweets: {0}'.format(results['retweets']))
	print('Parsed: {0}'.format(len(results['media'])))

	with open(outputFile, 'w') as file:
		json.dump(results, file, indent=4, default=lambda x:str(x))