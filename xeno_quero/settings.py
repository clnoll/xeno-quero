import os


CONCURRENT_LIMIT = os.getenv('CONCURRENT_LIMIT', 4)
RECORDINGS_URL = 'http://www.xeno-canto.org/api/2/recordings'
THREAD_LIMIT = 40
XENOCANTO_DATA_DIRECTORY = os.getenv('XENOCANTO_DATA_DIRECTORY')
