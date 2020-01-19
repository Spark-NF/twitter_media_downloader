# coding: utf-8

from ..src.parser import parse_tweet


class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)

user = Struct(**{
    'id_str': '456789',
    'name': 'Super user',
    'screen_name': 'superuser123',
})
tweet = Struct(**{
    'id_str': '123456',
    'created_at': '2019-06-24 20:19:35',
    'full_text': 'Hello world!',
    'entities': {
        'urls': [
            { 'expanded_url': 'https://instagram.com/test' },
            { 'expanded_url': 'https://www.google.com' },
            { 'expanded_url': 'https://periscope.tv/test' }
        ]
    },
    'user': user,
    'extended_entities': {
        'media': [
            {
                'video_info': {
                    'variants': [
                        {
                            'bitrate': 123,
                            'url': 'video_123'
                        },
                        {
                            'bitrate': 789,
                            'url': 'video_789'
                        }
                    ]
                }
            },
            {
                'media_url_https': 'video_789/video_thumb',
                'sizes': ['thumb', 'large']
            },
            {
                'media_url_https': 'my_image',
                'sizes': ['thumb', 'large']
            },
            {
                'media_url_https': 'other_image',
                'sizes': ['thumb', 'medium']
            }
        ]
    }
})
text_tweet = Struct(**{
    'id_str': '123456',
    'created_at': '2019-06-24 20:19:35',
    'user': user,
    'full_text': 'Hello world!'
})
retweet = Struct(**{
    'id_str': '789',
    'created_at': '2019-06-22 12:12:12',
    'user': user,
    'retweeted_status': tweet
})

def test_tweet():
    results = {
        'tweets': 0,
        'retweets': 0,
        'media': []
    }
    parse_tweet(tweet, True, 'large', results)
    assert results['tweets'] == 1
    assert results['retweets'] == 0
    assert len(results['media']) == 1
    assert results['media'][0]['tweet_id'] == '123456'
    assert results['media'][0]['original_tweet_id'] == '123456'
    assert results['media'][0]['text'] == ''
    assert results['media'][0]['videos'] == ['video_789']
    assert results['media'][0]['images'] == ['my_image:large', 'other_image']
    assert results['media'][0]['urls']['periscope'] == ['https://periscope.tv/test']
    assert results['media'][0]['urls']['instagram'] == ['https://instagram.com/test']
    assert results['media'][0]['urls']['others'] == ['https://www.google.com']

def test_text_tweet():
    results = {
        'tweets': 0,
        'retweets': 0,
        'media': []
    }
    parse_tweet(text_tweet, True, 'large', results)
    assert results['tweets'] == 1
    assert results['retweets'] == 0
    assert len(results['media']) == 1
    assert results['media'][0]['tweet_id'] == '123456'
    assert results['media'][0]['original_tweet_id'] == '123456'
    assert results['media'][0]['text'] == 'Hello world!'

def test_retweet():
    results = {
        'tweets': 0,
        'retweets': 0,
        'media': []
    }
    parse_tweet(retweet, True, 'large', results)
    assert results['tweets'] == 0
    assert results['retweets'] == 1
    assert len(results['media']) == 1
    assert results['media'][0]['tweet_id'] == '789'
    assert results['media'][0]['original_tweet_id'] == '123456'

def test_retweet_disabled():
    results = {
        'tweets': 0,
        'retweets': 0,
        'media': []
    }
    parse_tweet(retweet, False, 'large', results)
    assert results['tweets'] == 1
    assert results['retweets'] == 0
    assert len(results['media']) == 1
    assert results['media'][0]['tweet_id'] == '789'
    assert results['media'][0]['original_tweet_id'] == '789'
