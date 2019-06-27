#!/usr/bin/env python
# coding: utf-8

import os.path
import sys

# Import local functions
from src.args import parse_args
from src.config import get_oauth
from src.parser import get_medias
from src.mapper import generate_results
from src.downloader import download


if __name__ == '__main__':
    # Parse program arguments
    args = parse_args(sys.argv[1:])

    # Twitter OAuth
    auth = get_oauth('.oauth.json')

    # Create output directory if necessary
    outputDir = os.path.join(args.output, args.userid + os.sep if args.o_userid else '')
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)

    # Suppress output if the "quiet" flag is enabled
    if args.quiet:
        sys.stdout = open(os.devnull, 'w')

    # Start the download
    medias = get_medias(auth, args.userid, args.retweets, args.image_size, args.since, args.since_id, args.until, args.until_id)
    results = generate_results(medias, args.format)
    download(results, outputDir, False, False)
