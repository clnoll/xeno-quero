import os
from setuptools import setup, find_packages


ROOTDIR = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(ROOTDIR, 'xeno_quero', 'VERSION')) as f:
    version = str(f.read().strip())


setup(
    name='xeno_quero',
    version=version,
    description='Client library for the Xeno-canto API.',
    packages=find_packages(),
    install_requires=[
        'aiohttp==3.6.2'
        'paco==0.2.3',
        'requests==2.22.0'
    ],
    include_package_data=True,
    entry_points={"console_scripts": ["xeno-quero = xeno_quero.query:main"]},
)
