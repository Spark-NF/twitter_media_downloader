# coding: utf-8

from __future__ import print_function
import os
import requests
from tqdm import tqdm


def download(data, output_dir, stream, show_already_exists):
    """Download all files referenced in data"""
    # Count all entities in input file
    total = len(data['files']) + len(data['text'])
    for url_type in data['urls']:
        total += len(data['urls'][url_type])

    # Show input summary
    print('Files: {0}'.format(len(data['files'])))
    print('Urls:')
    print('- periscope: {0}'.format(len(data['urls']['periscope'])))
    print('- instagram: {0}'.format(len(data['urls']['instagram'])))
    print('- others: {0}'.format(len(data['urls']['others'])))
    print('Text only: {0}'.format(len(data['text'])))
    print('Total: {0}'.format(total))

    # Download all files
    for filename, url in data['files'].items():
        path = os.path.join(output_dir, filename)

        # Ignore already downloaded files
        if os.path.exists(path) and os.path.getsize(path) > 0:
            if show_already_exists:
                print('{0}: already exists'.format(filename))
            continue

        # Create directory if necessary
        path_dir = os.path.dirname(path)
        if not os.path.exists(path_dir):
            os.makedirs(path_dir)

        request = requests.get(url, stream=stream)
        total_length = request.headers.get('content-length')

        with open(path, 'wb') as file_descriptor:
            if not stream or total_length is None:
                file_descriptor.write(request.content)
                print('{0}: ok'.format(filename))
            else:
                # Progress bar
                for progress in tqdm(iterable=request.iter_content(), unit='b', unit_scale=True, total=int(total_length), desc=filename):
                    file_descriptor.write(progress)

    # Download periscope
    if data['urls']['periscope']:
        try:
            from pyriscope import processor
            processor.process(data['urls']['periscope'])
        except ImportError:
            print('You need the `{0}` module to download Periscope videos'.format('pyriscope'))
