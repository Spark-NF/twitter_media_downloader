# -*- coding: utf-8 -*-

"""
Loads and parses tweets using the Twitter API.
"""

from datetime import datetime
from typing import Any, Dict
import tweepy
from tqdm import tqdm
from .medias import VideoMedia


def parse_tweet(tweet: tweepy.models.Status, include_retweets: bool, image_size: str, results: Dict[str, Any]) -> None:
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
                        print(f'Size `{image_size}` not found for image `{media["media_url_https"]}`')
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


def get_medias(auth: Dict[str, str], user_id: str, include_retweets: bool, image_size: str, since: datetime, since_id: int, until: datetime, until_id: int, likes: bool) -> Dict[str, Any]:
    """Get all medias for a given Twitter user."""
    tweepy_auth = tweepy.OAuthHandler(auth['consumer_key'], auth['consumer_secret'])
    if 'access_token' in auth and 'access_token_secret' in auth:
        tweepy_auth.set_access_token(auth['access_token'], auth['access_token_secret'])

    api = tweepy.API(tweepy_auth, wait_on_rate_limit=True)

    results = {
        'tweets': 0,
        'retweets': 0,
        'media': []
    }
    capi = api.get_favorites if likes else api.user_timeline
    kwargs = {"include_entities": True} if likes else {}
    pbar = tqdm(desc='Resolving', unit=' tweets')
    for tweet in tweepy.Cursor(capi, user_id=user_id, include_rts=include_retweets, tweet_mode='extended', since_id=since_id, max_id=until_id, **kwargs).items():
        if since is not None and tweet.created_at < since:
            break
        if until is not None and tweet.created_at > until:
            continue
        pbar.update(1)
        parse_tweet(tweet, include_retweets, image_size, results)
    pbar.close()

    print(f'Link to user account: https://twitter.com/{user_id}')
    print(f'Medias for user {user_id}')
    print(f'- Tweets: {results["tweets"]}')
    print(f'- Retweets: {results["retweets"]}')
    print(f'- Parsed: {len(results["media"])}')

    return results
