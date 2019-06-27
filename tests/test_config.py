# coding: utf-8

import json
import mock
import os
from ..src import config
from ..src.config import get_oauth


testFile = 'test_oauth.json'

def test_get_oauth_prompt(mocker):
    if os.path.exists(testFile):
        os.remove(testFile)
    with mock.patch(config.__name__ + '.read', side_effect=['my_token', 'my_secret']):
        assert get_oauth(testFile) == {
            'consumer_token': 'my_token',
            'consumer_secret': 'my_secret'
        }

def test_get_oauth_read(mocker):
    auth = {
        'consumer_token': 'my_token',
        'consumer_secret': 'my_secret'
    }
    with open(testFile, 'w') as file:
        json.dump(auth, file)
    assert get_oauth(testFile) == auth
