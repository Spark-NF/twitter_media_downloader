# coding: utf-8

import json
import os
import mock
from ..src import config
from ..src.config import get_oauth


TEST_FILE = 'test_oauth.json'


def test_get_oauth_prompt():
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)
    with mock.patch(config.__name__ + '.read', side_effect=['my_token', 'my_secret']):
        assert get_oauth(TEST_FILE) == {
            'consumer_token': 'my_token',
            'consumer_secret': 'my_secret'
        }


def test_get_oauth_read():
    auth = {
        'consumer_token': 'my_token',
        'consumer_secret': 'my_secret'
    }
    with open(TEST_FILE, 'w') as file_descriptor:
        json.dump(auth, file_descriptor)
    assert get_oauth(TEST_FILE) == auth
