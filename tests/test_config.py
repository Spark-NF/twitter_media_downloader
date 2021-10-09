# coding: utf-8

"""
Unit tests for the config module.
"""

import json
import os
import mock
from ..src import config
from ..src.config import get_oauth


TEST_FILE = 'test_oauth.json'


def test_get_oauth_prompt():
    """Ensure that the user prompt for its OAuth credentials works correctly."""
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)
    with mock.patch(config.__name__ + '.read', side_effect=['my_key', 'my_secret', 'my_token', 'my_token_secret']):
        assert get_oauth(TEST_FILE) == {
            'consumer_key': 'my_key',
            'consumer_secret': 'my_secret',
            'access_token': 'my_token',
            'access_token_secret': 'my_token_secret'
        }


def test_get_oauth_read():
    """Ensure that the get_oauth function properly returns the contents of the JSON auth config file."""
    auth = {
        'consumer_key': 'my_key',
        'consumer_secret': 'my_secret',
        'access_token': 'my_token',
        'access_token_secret': 'my_token_secret'
    }
    with open(TEST_FILE, 'w') as file_descriptor:
        json.dump(auth, file_descriptor)
    assert get_oauth(TEST_FILE) == auth


def test_get_oauth_rename_consumer_token_to_consumer_key():
    """Ensure that the get_oauth function properly returns the contents of the JSON auth config file."""
    before = {
        'consumer_token': 'my_key',
        'consumer_secret': 'my_secret'
    }
    after = {
        'consumer_key': 'my_key',
        'consumer_secret': 'my_secret'
    }
    with open(TEST_FILE, 'w') as file_descriptor:
        json.dump(before, file_descriptor)
    assert get_oauth(TEST_FILE) == after
