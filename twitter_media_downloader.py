#!/usr/bin/env python
# coding: utf-8

import os.path
import sys
import csv

# Import local functions
from src.args import parse_args, parse_file_arg
from src.config import get_oauth
from src.parser import get_medias
from src.mapper import generate_results
from src.downloader import download


if __name__ == '__main__':
    # Parse program arguments
    args = parse_args(sys.argv[1:])

    user_ids = []

    if (len(args.userid) == 0 and args.csv is None) or (len(args.userid) > 0 and args.csv is not None):
        raise Exception('You need to either provider a csv or list of userIds')
    elif len(args.userid) > 0:
        user_ids = parse_file_arg(args.userid)
    elif args.csv is not None:
        if not os.access(args.csv, os.R_OK):
            raise Exception('Could not read file ' + args.csv)

        with open(args.csv) as csv_file:
            csv_reader = csv.DictReader(csv_file)

            for row in csv_reader:
                user_ids.append(row['userId'])

    # Twitter OAuth
    auth = get_oauth('.oauth.json')

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
