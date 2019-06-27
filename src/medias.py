# coding: utf-8

class VideoMedia(object):
    def bitrate(self):
        return self.obj['bitrate'] if 'bitrate' in self.obj else 0

    def __init__(self, obj):
        self.obj = obj

    def __lt__(self, other):
        return self.bitrate() < other.bitrate()

    def __le__(self, other):
        return self.bitrate() <= other.bitrate()

    def __eq__(self, other):
        return self.bitrate() == other.bitrate()
