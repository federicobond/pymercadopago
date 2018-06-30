#!/usr/bin/env python

import os
import re

from codecs import open
from setuptools import find_packages, setup


with open('mercadopago/__init__.py', 'r', encoding='utf-8') as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)


def read(fname):
    path = os.path.join(os.path.dirname(__file__), fname)
    with open(path, 'r', 'utf-8') as f:
        return f.read()


setup(
    name="pymercadopago",
    version=version,
    description="An API wrapper for MercadoPago",
    long_description=read('README.rst'),
    long_description_content_type='text/x-rst',
    author="Federico Bond",
    author_email="federicobond@gmail.com",
    url="https://github.com/federicobond/pymercadopago",
    license='Apache 2.0',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    install_requires=[
        "requests>=2.1.0",
        "future",
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        "pytest",
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='mercadopago api'
)
