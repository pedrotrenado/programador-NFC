#!/usr/bin/env python

from setuptools import find_namespace_packages
from setuptools import setup

setup(
    name="mfrc630",
    version="0.0.1",
    license="propietary and confidential",
    author="TycheTools",
    maintainer="TycheTools FW team",
    description="API for MFRC630 card reader developed for TycheTools sensors.",
    url="https://bitbucket.org/tychermo/mfrc630_python",
    packages=find_namespace_packages(include=["mfrc630"]),
    install_requires=[
        "spidev",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)
