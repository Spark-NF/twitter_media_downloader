#!/usr/bin/env python
# coding: utf-8

import os.path
import sys

# Import local functions
from src.args import parse_args, parse_file_arg
from src.config import get_oauth
from src.parser import get_medias
from src.mapper import generate_results
from src.downloader import download


if __name__ == '__main__':
    # Parse program arguments
    ARGS = parse_args(sys.argv[1:])
    USER_IDS = parse_file_arg(ARGS.userid)

    # Twitter OAuth
    AUTH = get_oauth('.oauth.json')

    # Suppress output if the "quiet" flag is enabled
    if ARGS.quiet:
        sys.stdout = open(os.devnull, 'w')

    # For each user in the ID list
    for user_id in USER_IDS:

        # Create output directory if necessary
        outputDir = os.path.join(ARGS.output, user_id + os.sep if ARGS.o_userid else '')
        if not os.path.exists(outputDir):
            os.makedirs(outputDir)

        # Start the download
        medias = get_medias(AUTH, user_id, ARGS.retweets, ARGS.image_size, ARGS.since, ARGS.since_id, ARGS.until, ARGS.until_id, ARGS.likes)
        results = generate_results(medias, ARGS.format)
        download(results, outputDir, False, True)
