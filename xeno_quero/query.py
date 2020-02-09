import argparse
import json

import requests

from xeno_quero import settings
from xeno_quero.client import Client


def main():
    parser = argparse.ArgumentParser(description='Query Xeno-canto.')
    parser.add_argument(
        '-q', '--query',
        type=str,
        required=True,
        help='Xeno-canto query as specified here: https://www.xeno-canto.org/article/153.',
    )
    parser.add_argument(
        '-d', '--directory',
        type=str,
        required=False,
        help='Directory in which to '
             '1) check for existing recordings, and '
             '2) save query results. '
             'If not set, results will be printed to STDOUT.\n'
             'Can also be set as an environment variable.',
    )
    parser.add_argument(
        '-m', '--metadata-only',
        action='store_true',
        help='Download the metadata only.\n'
             'Defaults to false unless a download directory is not specified.'
    )
    parser.add_argument(
        '-o', '--overwrite',
        action='store_true',
        help='Overwrite existing recordings.\n'
             'Defaults to false.',
    )
    parser.add_argument(
        '-s', '--summary',
        action='store_true',
        help='Print a summary of the query results.\n'
             'Defaults to false.',
    )

    args = parser.parse_args()
    query = args.query
    directory = args.directory or settings.XENOCANTO_DATA_DIRECTORY
    metadata_only = args.metadata_only if directory else True
    overwrite = args.overwrite
    summary = args.summary

    client = Client(directory=directory)

    try:
        print(client.query(query, metadata_only=metadata_only, overwrite=overwrite, summary=summary))
    except requests.exceptions.HTTPError as exc:
        print('Error querying Xeno-canto:')
        print(json.loads(exc.response.content.decode('utf-8')))

if __name__ == '__main__':
    main()
