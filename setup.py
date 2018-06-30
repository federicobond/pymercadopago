#!/usr/bin/env python

import os

from setuptools import find_packages, setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="pymercadopago",
    version="0.1.2",
    description="An API wrapper for MercadoPago",
    long_description=read('README.rst'),
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
