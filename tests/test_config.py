# coding: utf-8

import json
import mock
import os
from ..src import config
from ..src.config import getOAuth


testFile = 'test_oauth.json'

def test_getOAuth_prompt(mocker):
	os.remove(testFile)
	with mock.patch(config.__name__ + '.read', side_effect=['my_token', 'my_secret']):
		assert getOAuth(testFile) == {
			'consumer_token': 'my_token',
			'consumer_secret': 'my_secret'
		}

def test_getOAuth_read(mocker):
	auth = {
		'consumer_token': 'my_token',
		'consumer_secret': 'my_secret'
	}
	with open(testFile, 'w') as file:
		json.dump(auth, file)
	assert getOAuth(testFile) == auth