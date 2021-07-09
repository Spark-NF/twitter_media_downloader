# coding: utf-8

"""
Unit tests for the medias module.
"""

from ..src.medias import VideoMedia


def test_bitrate_missing():
    """Ensure that the bitrate method works when bitrate is missing."""
    assert VideoMedia({}).bitrate() == 0


def test_bitrate_ok():
    """Ensure that the bitrate method works when bitrate is provided."""
    assert VideoMedia({'bitrate': 123}).bitrate() == 123


def test_equals():
    """Ensure that the equality operator works with instances with same/different bitrates."""
    assert VideoMedia({'bitrate': 123}) != VideoMedia({'bitrate': 456})
    assert VideoMedia({'bitrate': 123}) == VideoMedia({'bitrate': 123})


def test_compare():
    """Ensure that the comparison operators works with instances with same/different bitrates."""
    assert VideoMedia({'bitrate': 123}) < VideoMedia({'bitrate': 456})
    assert VideoMedia({'bitrate': 789}) > VideoMedia({'bitrate': 456})
    assert VideoMedia({'bitrate': 123}) <= VideoMedia({'bitrate': 123})
    assert VideoMedia({'bitrate': 123}) >= VideoMedia({'bitrate': 123})
