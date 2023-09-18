# coding: utf-8

"""
Takes a list of parsed tweets and generate list of files to download and their target location.
"""

import re
from datetime import datetime
from os.path import splitext, basename
from typing import Any, Dict, Union

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse


def is_unicode(value: str) -> bool:
    """Checks if a string is an unicode string."""
    try:
        return isinstance(value, unicode)
    except NameError:
        return isinstance(value, str)


def slugify(value: str) -> str:
    """Converts a string with special characters to a string without that can more easily be used as a filename."""
    if is_unicode(value):
        import unicodedata
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub('[<>/\\:"|?*]', '-', value).strip().lower()
    return value


def date_to_string(value: Union[str, datetime]) -> str:
    """Converts a datetime instance to a string."""
    if isinstance(value, str):
        return value
    return value.strftime('%Y-%m-%d %H-%M-%S')


def parse_filename(filename_format: str, tokens: Dict[str, Union[str, datetime]], url: str) -> str:
    """Uses a list of tokens and a filename format to generate a filename."""
    disassembled = urlparse(url)
    full_filename = basename(disassembled.path)
    full_filename = re.sub(':(?:thumb|small|medium|large|orig)$', '', full_filename)
    filename, ext = splitext(full_filename)
    replaced = filename_format.replace('%date%', slugify(date_to_string(tokens['date']))) \
        .replace('%original_date%', slugify(date_to_string(tokens['original_date']))) \
        .replace('%filename%', slugify(filename)) \
        .replace('%ext%', slugify(ext[1:]))
    for key in ['tweet_id', 'original_tweet_id', 'user_id', 'original_user_id', 'user_name', 'original_user_name', 'user_screen_name', 'original_user_screen_name', 'type']:
        if key in tokens:
            value = tokens[key]
            str_value = date_to_string(value) if isinstance(value, datetime) else value
            replaced = replaced.replace('%' + key + '%', slugify(str_value))
    return replaced


def generate_results(data: Dict[str, Any], filename_format: str) -> Dict[str, Any]:
    """Takes a list of tweet information and generate a list of files to download and their target location."""
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
            filename = parse_filename(filename_format, media, url)
            results['files'][filename] = url

    return results
