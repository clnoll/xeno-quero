import json
import os
import time
from multiprocessing.pool import ThreadPool
from urllib import request

import aiohttp
import paco

from xeno_quero import settings

global TOTAL
TOTAL = 0


async def _fetch_content(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as res:
            return await res.content.read()


async def _fetch_urls(urls):
    data = []
    responses = await paco.map(_fetch_content, urls, limit=settings.CONCURRENT_LIMIT)

    for res in responses:
        data.append(json.loads(res))

    return data


def fetch_urls(urls):
    return paco.run(_fetch_urls(urls))


def _download(url, filepath):
    filepath.parent.mkdir(parents=True, exist_ok=True)
    request.urlretrieve(url, filepath)
    time.sleep(5)


def _download_if_not_exists(url, filepath):
    global TOTAL

    if os.path.exists(filepath):
        return
    else:
        _download(url, filepath)
        TOTAL += 1


def download_multi(urls_filepaths, overwrite=False):
    global TOTAL
    TOTAL = 0

    pool = ThreadPool(settings.THREAD_LIMIT)
    if overwrite:
        pool.starmap(_download, urls_filepaths)
        return len(urls_filepaths)
    else:
        pool.starmap(_download_if_not_exists, urls_filepaths)
        return TOTAL


def _write(data, filepath):
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'w') as fp:
        json.dump(data, fp)


def _write_if_not_exists(data, filepath):
    global TOTAL

    if os.path.exists(filepath):
        return
    else:
        _write(data, filepath)
        TOTAL += 1


def write_multi(data_filepaths, overwrite=False):
    global TOTAL
    TOTAL = 0

    pool = ThreadPool(settings.THREAD_LIMIT)
    if overwrite:
        pool.starmap(_write, data_filepaths)
        return len(data_filepaths)
    else:
        pool.starmap(_write_if_not_exists, data_filepaths)
        return TOTAL
