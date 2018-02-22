import tweepy
import json
import os


class VideoMedia:
	def bitrate(self):
		return self.obj['bitrate'] if 'bitrate' in self.obj else 0

	def __init__(self, obj):
		self.obj = obj

	def __lt__(self, other):
		return self.bitrate() < other.bitrate()

	def __eq__(self, other):
		return self.bitrate() == other.bitrate()

def getMedias(auth, userId, includeRetweets, imageSize, outputFile):
	auth = tweepy.OAuthHandler(auth['consumer_token'], auth['consumer_secret'])
	api = tweepy.API(auth)

	results = {
		'media': []
	}
	retweets = 0
	tweets = 0
	for tweet in tweepy.Cursor(api.user_timeline, id=userId, include_rts=includeRetweets, include_entities=True, tweet_mode='extended').items():
		urls = {
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
			urls['original_date'] = tweet.created_at
			retweets += 1
		else:
			tweets += 1

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
			urls['images'] = []

		if len(urls['videos']) == 0 and len(urls['images']) == 0 and len(urls['urls']['periscope']) == 0 and len(urls['urls']['instagram']) == 0:
			urls['text'] = tweet.full_text

		results['media'].append(urls)

	print('Tweets: {0}'.format(tweets))
	print('Retweets: {0}'.format(retweets))
	print('Parsed: {0}'.format(len(results['media'])))

	with open(outputFile, 'w') as file:
		json.dump(results, file, indent=4, default=lambda x:str(x))