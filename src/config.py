# coding: utf-8

"""
Helper methods to get the user's OAuth credentials.
"""

import json
import os.path

try:
    # pylint: disable=redefined-builtin,invalid-name
    input = raw_input
except NameError:
    pass


def read(msg):
    """Wrapper around the input module for easier mock-ing."""
    return input(msg)


def get_oauth(path):
    """Loads the OAuth credentials from the file if it exists, otherwise asks the user for them."""
    if os.path.exists(path):
        data = open(path).read()
        return json.loads(data)

    auth = {
        'consumer_token': '',
        'consumer_secret': ''
    }
    auth['consumer_token'] = read('Token: ')
    auth['consumer_secret'] = read('Secret: ')

    with open(path, 'w') as oauth_file:
        json.dump(auth, oauth_file, indent=4, default=str)

    return auth
