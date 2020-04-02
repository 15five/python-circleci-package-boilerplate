#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:copyright: (c) 2017 by Lev Lazinskiy
:license: MIT, see LICENSE for more details.
"""

from setuptools import setup, find_packages

VERSION = "0.1.3"


setup(
    name="healthchecks_manager",
    version=VERSION,
    description="Library for automatic registration and pinging of https://healthchecks.io/ healthchecks.",
    long_description="see repo for readme",
    url="https://github.com/15five/healthchecks-manager",
    author="Caleb Sparks",
    author_email="caleb@15five.com",
    license="MIT",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    keywords="healthchecks healthchecks.io registration creation",
    packages=find_packages(),
    install_requires=["requests==2.20.1",],
    python_requires=">=3",
)
