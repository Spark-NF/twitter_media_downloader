# coding: utf-8

"""
Loads and parses tweets using the Twitter API.
"""

from __future__ import print_function
import tweepy
from tqdm import tqdm
from .medias import VideoMedia


def parse_tweet(tweet, include_retweets, image_size, results):
    """Parse a single tweet, returning a more useful structure containing its medias."""
    urls = {
        'tweet_id': tweet.id_str,
        'original_tweet_id': tweet.id_str,
        'date': tweet.created_at,
        'original_date': tweet.created_at,
        'user_id': tweet.user.id_str,
        'user_name': tweet.user.name,
        'user_screen_name': tweet.user.screen_name,
        'original_user_id': tweet.user.id_str,
        'original_user_name': tweet.user.name,
        'original_user_screen_name': tweet.user.screen_name,
        'type': 'tweet',
        'videos': [],
        'images': [],
        'urls': {
            'periscope': [],
            'instagram': [],
            'others': []
        },
        'text': ''  # tweet.full_text
    }

    if include_retweets and hasattr(tweet, 'retweeted_status'):
        tweet = tweet.retweeted_status
        urls['original_tweet_id'] = tweet.id_str
        urls['original_date'] = tweet.created_at
        urls['original_user_id'] = tweet.user.id_str
        urls['original_user_name'] = tweet.user.name
        urls['original_user_screen_name'] = tweet.user.screen_name
        urls['type'] = 'retweet'
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
                    if image_size in media['sizes'] or image_size == 'orig':
                        url += ":" + image_size
                    else:
                        print('Size `{0}` not found for image `{1}`'.format(image_size, media['media_url_https']))
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
    if len(urls['videos']) == 1 and urls['images'] and 'video_thumb' in urls['images'][0]:
        urls['images'] = urls['images'][1:]

    if not urls['videos'] and not urls['images'] and not urls['urls']['periscope'] and not urls['urls']['instagram'] and hasattr(tweet, 'full_text'):
        urls['text'] = tweet.full_text

    results['media'].append(urls)


def get_medias(auth, user_id, include_retweets, image_size, since, since_id, until, until_id, likes):
    """Get all medias for a given Twitter user."""
    auth = tweepy.OAuthHandler(auth['consumer_token'], auth['consumer_secret'])
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    results = {
        'tweets': 0,
        'retweets': 0,
        'media': []
    }
    capi = api.favorites if likes else api.user_timeline
    pbar = tqdm(desc='Resolving', unit=' tweets')
    for tweet in tweepy.Cursor(capi, id=user_id, include_rts=include_retweets, include_entities=True, tweet_mode='extended', since_id=since_id, max_id=until_id).items():
        if since is not None and tweet.created_at < since:
            break
        if until is not None and tweet.created_at > until:
            continue
        pbar.update(1)
        parse_tweet(tweet, include_retweets, image_size, results)
    pbar.close()

    print('Medias for user {0}'.format(user_id))
    print('- Tweets: {0}'.format(results['tweets']))
    print('- Retweets: {0}'.format(results['retweets']))
    print('- Parsed: {0}'.format(len(results['media'])))

    return results
