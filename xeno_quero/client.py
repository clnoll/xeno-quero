import json
from pathlib import Path

import requests

from xeno_quero.settings import RECORDINGS_URL, XENOCANTO_DATA_DIRECTORY
from xeno_quero.utils import download_multi, fetch_urls, write_multi


class Client:
    def __init__(self, directory=None):
        self.directory = Path(directory or XENOCANTO_DATA_DIRECTORY)

    def query(self, query, summary=False, metadata_only=False, overwrite=False):
        '''
        {
            "numRecordings":"1",
            "numSpecies":"1",
            "page":1,
            "numPages":1,
            "recordings":[
                ...,
                Array of Recording objects (see below),
                ...
                ]
        }
        '''
        self.base_url = RECORDINGS_URL
        data = self._query(query)

        if summary:
            n_page_recordings = len(data.pop('recordings', []))
            if 'page=' not in query:
                data.pop('page', None)
            else:
                data['numRecordingsOnPage'] = n_page_recordings

            return data

        return self.get_recordings(
            data['recordings'],
            query=query,
            page=data['page'],
            n_pages=data['numPages'],
            metadata_only=metadata_only,
            overwrite=overwrite
        )

    def download(self, recordings, metadata_only=False, overwrite=False):
        if not self.directory:
            raise ValueError('Please specify a directory for downloaded files.')

        n_meta_downloaded = self.download_meta(recordings, overwrite=overwrite)

        if metadata_only:
            return (n_meta_downloaded, 0)

        n_recordings_downloaded = self.download_recordings(recordings, overwrite=overwrite)

        return n_meta_downloaded, n_recordings_downloaded

    def get_recordings(self, recordings, query, page, n_pages, metadata_only=False, overwrite=False):
        if 'page=' not in query and page < n_pages:
            urls = [f'{self.base_url}?query={query}&page={p}' for p in range(page, n_pages)]
            for response in fetch_urls(urls):
                if 'recordings' in response:
                    recordings.extend(response['recordings'])
                else:
                    print(f'error: {response}')

        if not self.directory:
            return recordings

        n_meta, n_downloads = self.download(
            recordings,
            metadata_only=metadata_only,
            overwrite=overwrite
        )

        return f'{n_meta} metadata files saved.\n' \
               f'{n_downloads} recordings downloaded. '

    def download_meta(self, recordings, overwrite=False):
        data_filepaths = [
            (r, self.directory / f'{r["gen"]}-{r["sp"]}' / f'{r["id"]}.json') for r in recordings
        ]
        print(f'Downloading up to {len(recordings)} recording metadata files.')
        return write_multi(data_filepaths, overwrite=overwrite)

    def download_recordings(self, recordings, overwrite=False):
        urls_filepaths = [
            (
                f'http:{r["file"]}',
                self.directory / f'{r["gen"]}-{r["sp"]}' / f'{r["id"]}.mp3',
            )
            for r in recordings
        ]

        print(f'Downloading up to {len(recordings)} recordings.')
        return download_multi(urls_filepaths, overwrite=overwrite)

    def _query(self, query):
        resp = requests.get(f'{self.base_url}?query={query}')
        resp.raise_for_status()
        return json.loads(resp.content.decode('utf-8'))
