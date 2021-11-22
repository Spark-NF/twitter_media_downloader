
# coding: utf-8

"""
Unit tests for the downloader module.
"""

import mock
from ..src.downloader import download


def mocked_requests_get(*args):
    """Mock all requests HTTP calls by returning the URL as contents."""
    class MockResponse(object):
        """Mock response for the requests module."""
        def __init__(self, content, status_code):
            self.headers = dict()
            self.content = str.encode(content)
            self.status_code = status_code
    return MockResponse(args[0], 200)


def test_download():
    """Ensure that the download function works."""
    data = {
        'text': ['Hello world!'],
        'urls': {
            'periscope': ['https://periscope.tv/test'],
            'instagram': ['https://instagram.com/test'],
            'others': ['https://www.google.com']
        },
        'files': {
            '[2019-06-22 12-12-12] video_789.mp4': 'http://test.com/video_789.mp4',
            '[2019-06-22 12-12-12] my_image.png': 'http://test.com/my_image.png:large',
            '[2019-06-22 12-12-12] other_image.jpg': 'http://test.com/other_image.jpg'
        }
    }
    with mock.patch('requests.get', side_effect=mocked_requests_get):
        download(data, 'test_out/', False, True)
