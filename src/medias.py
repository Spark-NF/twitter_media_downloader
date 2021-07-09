# coding: utf-8

"""
Module to handle video medias.
"""


class VideoMedia(object):
    """Basic class that allows to compare video medias by bitrate."""

    def bitrate(self):
        """Return the video's bitrate if available, otherwise 0."""
        return self.obj['bitrate'] if 'bitrate' in self.obj else 0

    def __init__(self, obj):
        self.obj = obj

    def __lt__(self, other):
        return self.bitrate() < other.bitrate()

    def __le__(self, other):
        return self.bitrate() <= other.bitrate()

    def __eq__(self, other):
        return self.bitrate() == other.bitrate()
