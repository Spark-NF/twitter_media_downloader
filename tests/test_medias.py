# coding: utf-8

from ..src.medias import VideoMedia

def test_bitrate_missing():
    assert VideoMedia({}).bitrate() == 0

def test_bitrate_ok():
    assert VideoMedia({'bitrate': 123}).bitrate() == 123

def test_equals():
    assert VideoMedia({'bitrate': 123}) != VideoMedia({'bitrate': 456})
    assert VideoMedia({'bitrate': 123}) == VideoMedia({'bitrate': 123})

def test_compare():
    assert VideoMedia({'bitrate': 123}) < VideoMedia({'bitrate': 456})
    assert VideoMedia({'bitrate': 789}) > VideoMedia({'bitrate': 456})
    assert VideoMedia({'bitrate': 123}) <= VideoMedia({'bitrate': 123})
    assert VideoMedia({'bitrate': 123}) >= VideoMedia({'bitrate': 123})
