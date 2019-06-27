# coding: utf-8

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

def date_to_string(value):
    if isinstance(value, str):
        return value
    return value.strftime('%Y-%m-%d %H-%M-%S')

def parse_filename(format, tweet_id, original_tweet_id, date, original_date, url):
    disassembled = urlparse(url)
    file = basename(disassembled.path)
    file = re.sub(':(?:thumb|small|medium|large)$', '', file)
    filename, ext = splitext(file)
    replaced = format.replace('%date%', date_to_string(date)) \
        .replace('%original_date%', date_to_string(original_date)) \
        .replace('%tweet_id%', tweet_id) \
        .replace('%original_tweet_id%', original_tweet_id) \
        .replace('%filename%', filename) \
        .replace('%ext%', ext[1:])
    slugified = slugify(replaced)
    return slugified

def generate_results(data, filename_format):
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
        for url_type in media['urls']:
            for url in media['urls'][url_type]:
                results['urls'][url_type].append(url)

        # Files
        for url in media['images'] + media['videos']:
            filename = parse_filename(filename_format, media['tweet_id'], media['original_tweet_id'], media['date'], media['original_date'], url)
            results['files'][filename] = url

    return results
