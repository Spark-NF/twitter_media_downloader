#!/usr/bin/env python3

import setuptools

setuptools.setup(
    name="twitter_media_downloader",
    version="20200217",
    license="MIT",
    url="https://github.com/la-snesne/twitter_media_downloader",
    keywords="Twitter",
    description="Twitter media downloader",
    install_requires=["requests", "tweepy", "tqdm"],
    entry_points = {
        'console_scripts': [
        'twt-media-dl = twt-media-dl.twitter_media_downloader:main']}
)
