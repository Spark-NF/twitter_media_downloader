# coding: utf-8

import io
import json
import os.path

try: input = raw_input
except NameError: pass


# Used for easier mock-ing
def read(msg):
    return input(msg)

def getOAuth(path):
    if not os.path.exists(path):
        auth = {
            'consumer_token': '',
            'consumer_secret': ''
        }
        auth['consumer_token'] = read('Token: ')
        auth['consumer_secret'] = read('Secret: ')

        with open(path, 'w') as file:
            json.dump(auth, file, indent=4, default=lambda x:str(x))

        return auth
    else:
        data = open(path).read()
        return json.loads(data)
