# coding: utf-8

from datetime import datetime
from ..src.mapper import slugify, parse_filename, generate_results


def test_slugify_basic():
    assert slugify(u'test') == 'test'

def test_slugify_hard():
    assert slugify(u'héhé/test?') == 'hehe-test-'

def test_parse_filename():
    tokens = {
        'date': '2019-06-27 11:25:12',
        'original_date': '2019-06-27 11:25:12'
    }
    assert parse_filename(u'[%date%] %filename%.%ext%', tokens, 'https://test.com/my_image.png:large') == '[2019-06-27 11-25-12] my_image.png'

    tokens = {
        'date': '2019-06-27 11:25:12',
        'original_date': '2019-06-23 11:25:12',
        'type': 'retweet'
    }
    assert parse_filename(u'%type%/[%original_date%] %filename%.%ext%', tokens, 'https://test.com/oops') == 'retweet/[2019-06-23 11-25-12] oops.'

def test_generate_results():
    data = {
        'media': [
            {
                'tweet_id': '123',
                'original_tweet_id': '123',
                'date': datetime(2019, 6, 22, 12, 12, 12),
                'original_date': datetime(2019, 6, 22, 12, 12, 12),
                'type': 'tweet',
                'text': '',
                'videos': ['video_789.mp4'],
                'images': ['my_image.png:large', 'other_image.jpg'],
                'urls': {
                    'periscope': ['https://periscope.tv/test'],
                    'instagram': ['https://instagram.com/test'],
                    'others': ['https://www.google.com']
                }
            },
            {
                'tweet_id': '456',
                'original_tweet_id': '789',
                'date': datetime(2019, 6, 24, 12, 12, 12),
                'original_date': datetime(2019, 6, 23, 12, 12, 12),
                'type': 'retweet',
                'text': 'Hello world!',
                'videos': [],
                'images': [],
                'urls': {
                    'periscope': [],
                    'instagram': [],
                    'others': []
                }
            }
        ]
    }
    assert generate_results(data, u'[%date%] %filename%.%ext%') == {
        'text': ['Hello world!'],
        'urls': {
            'periscope': ['https://periscope.tv/test'],
            'instagram': ['https://instagram.com/test'],
            'others': ['https://www.google.com']
        },
        'files': {
            '[2019-06-22 12-12-12] video_789.mp4': 'video_789.mp4',
            '[2019-06-22 12-12-12] my_image.png': 'my_image.png:large',
            '[2019-06-22 12-12-12] other_image.jpg': 'other_image.jpg'
        }
    }
