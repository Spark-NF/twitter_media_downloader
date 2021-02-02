# coding: utf-8

import json
import os.path

try:
    # pylint: disable=redefined-builtin
    input = raw_input
except NameError:
    pass


# Used for easier mock-ing
def read(msg):
    return input(msg)


def get_oauth(path):
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
