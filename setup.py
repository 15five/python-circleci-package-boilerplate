#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:copyright: (c) 2017 by Lev Lazinskiy
:license: MIT, see LICENSE for more details.
"""
import os
import sys

from setuptools import setup, find_packages
from setuptools.command.install import install

VERSION = "0.1.0"


def readme():
    """print long description"""
    with open("README.md") as f:
        return f.read()


class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""

    description = "verify that the git tag matches our version"

    def run(self):
        tag = os.getenv("CIRCLE_TAG")

        if tag != VERSION:
            info = "Git tag: {0} does not match the version of this app: {1}".format(
                tag, VERSION
            )
            sys.exit(info)


setup(
    name="healthchecks_manager",
    version=VERSION,
    description="Library for automatic registration and pinging of https://healthchecks.io/ healthchecks.",
    long_description=readme(),
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
    cmdclass={"verify": VerifyVersionCommand,},
)
