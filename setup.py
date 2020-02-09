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
        'requests==2.22.0'
    ],
    include_package_data=True,
)
