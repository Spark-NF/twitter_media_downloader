# coding: utf-8

from ..src.mapper import slugify, parseFilename


def test_slugify_basic():
    assert slugify(u'test') == 'test'

def test_slugify_hard():
    assert slugify(u'héhé/test?') == 'hehe-test-'

def test_parseFilename():
    assert parseFilename(u'[%date%] %filename%.%ext%', '123', '456', '2019-06-27 11:25', '2019-06-27 11:25', 'https://test.com/my_image.png:large') == '[2019-06-27 11-25] my_image.png'
    assert parseFilename(u'[%original_date%] %filename%.%ext%', '123', '456', '2019-06-27 11:25', '2019-06-23 11:25', 'https://test.com/oops') == '[2019-06-23 11-25] oops.'