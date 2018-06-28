#!/usr/bin/env python
from setuptools import find_packages, setup

setup(
    name="mercadopago-redux",
    version="0.1.0",
    description="An API wrapper for MercadoPago",
    author="Federico Bond",
    author_email="federicobond@gmail.com",
    url="https://github.com/globality-corp/https://github.com/federicobond/mercadopago-redux",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "requests>=2.19.1",
    ],
    setup_requires=[
        "nose>=1.3.6",
    ],
    dependency_links=[
    ],
    entry_points={
    },
    tests_require=[
        "coverage>=3.7.1",
        "mock>=1.0.1",
        "PyHamcrest>=1.8.5",
    ],
)
