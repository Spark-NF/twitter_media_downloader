# coding: utf-8

"""
Module to handle video medias.
"""

from typing import Any, Dict


class VideoMedia:
    """Basic class that allows to compare video medias by bitrate."""

    def bitrate(self) -> int:
        """Return the video's bitrate if available, otherwise 0."""
        return self.obj['bitrate'] if 'bitrate' in self.obj else 0

    def __init__(self, obj: Dict[str, Any]) -> None:
        self.obj = obj

    def __lt__(self, other: object) -> bool:
        return isinstance(other, VideoMedia) and self.bitrate() < other.bitrate()

    def __le__(self, other: object) -> bool:
        return isinstance(other, VideoMedia) and self.bitrate() <= other.bitrate()

    def __eq__(self, other: object) -> bool:
        return isinstance(other, VideoMedia) and self.bitrate() == other.bitrate()
