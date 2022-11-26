import json
import os
import urllib
from multiprocessing.pool import ThreadPool

import aiohttp
import paco

from xeno_quero import settings

global TOTAL
TOTAL = 0

global url_fetch_errors
url_fetch_errors = {}

global download_errors
download_errors = {}


async def _fetch_content(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as res:
            try:
                return await res.content.read()
            except Exception as exc:
                import ipdb; ipdb.set_trace()
                raise exc


async def _fetch_urls(urls):
    data = []
    responses = await paco.map(_fetch_content, urls, limit=settings.CONCURRENT_LIMIT)

    for res in responses:
        data.append(json.loads(res))

    return data


def fetch_urls(urls):
    return paco.run(_fetch_urls(urls))


def _download(url_filepath):
    try:
        urllib.request.urlretrieve(*url_filepath)
    except urllib.error.URLError as exc:
        import ipdb; ipdb.set_trace()
        raise exc


def _download_if_not_exists(url_filepath):
    global TOTAL

    url, filepath = url_filepath
    if os.path.exists(filepath):
        return
    else:
        _download(url_filepath)
        TOTAL += 1


def download_multi(urls_filepaths, overwrite=False):
    global TOTAL
    TOTAL = 0

    pool = ThreadPool(settings.THREAD_LIMIT)
    if overwrite:
        pool.map(_download, urls_filepaths)
        return len(urls_filepaths)
    else:
        pool.map(_download_if_not_exists, urls_filepaths)
        return TOTAL


def _write(data_filepath):
    data, filepath = data_filepath
    with open(filepath, 'w') as fp:
        json.dump(data, fp)


def _write_if_not_exists(url_filepath):
    global TOTAL

    url, filepath = url_filepath
    if os.path.exists(filepath):
        return
    else:
        _write(url_filepath)
        TOTAL += 1


def write_multi(data_filepaths, overwrite=False):
    global TOTAL
    TOTAL = 0

    pool = ThreadPool(settings.THREAD_LIMIT)
    if overwrite:
        pool.map(_write, data_filepaths)
        return len(data_filepaths)
    else:
        pool.map(_write_if_not_exists, data_filepaths)
        return TOTAL
