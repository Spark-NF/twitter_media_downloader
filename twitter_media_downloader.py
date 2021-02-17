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
    args = parse_args(sys.argv[1:])
    user_ids = parse_file_arg(args.userid)

    # Twitter OAuth
    auth = get_oauth(args.credential)

    # Suppress output if the "quiet" flag is enabled
    if args.quiet:
        sys.stdout = open(os.devnull, 'w')

    # For each user in the ID list
    for user_id in user_ids:

        # Create output directory if necessary
        outputDir = os.path.join(args.output, user_id + os.sep if args.o_userid else '')
        if not os.path.exists(outputDir):
            os.makedirs(outputDir)

        # Start the download
        medias = get_medias(auth, user_id, args.retweets, args.image_size, args.since, args.since_id, args.until, args.until_id, args.likes)
        results = generate_results(medias, args.format)
        download(results, outputDir, False, True)
