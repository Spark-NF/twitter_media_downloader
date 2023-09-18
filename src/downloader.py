# coding: utf-8

"""
Downloads all files to their already-generated paths.
"""

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
    print(f'Files: {len(data["files"])}')
    print('Urls:')
    print(f'- periscope: {len(data["urls"]["periscope"])}')
    print(f'- instagram: {len(data["urls"]["instagram"])}')
    print(f'- others: {len(data["urls"]["others"])}')
    print(f'Text only: {len(data["text"])}')
    print(f'Total: {total}')

    # Download all files
    for filename, url in data['files'].items():
        path = os.path.join(output_dir, filename)

        # Ignore already downloaded files
        if os.path.exists(path) and os.path.getsize(path) > 0:
            if show_already_exists:
                print(f'{filename}: already exists')
            continue

        # Create directory if necessary
        path_dir = os.path.dirname(path)
        if not os.path.exists(path_dir):
            os.makedirs(path_dir)

        request = requests.get(url, stream=stream, timeout=30)
        total_length = request.headers.get('content-length')

        with open(path, 'wb') as file_descriptor:
            if not stream or total_length is None:
                file_descriptor.write(request.content)
                print(f'{filename}: ok')
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
            print('You need the `pyriscope` module to download Periscope videos')
