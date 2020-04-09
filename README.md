# python-package-boilerplate [![CircleCI](https://circleci.com/gh/15five/python-package-boilerplate.svg?style=svg&circle-token=11980ad9faf7cfe88b5812c880cfed05b867b0cb)](https://circleci.com/gh/15five/python-package-boilerplate) [![PyPI version](https://badge.fury.io/py/python-package-boilerplate.svg)](https://badge.fury.io/py/python-package-boilerplate)
boilerplate repo you can use as a base for your python package.

## Features:
* Package directory structure already laid out
* **FULL** CI/CD through circleci with the works (black linting, pip caching, tests against multiple python versions, test summary, coverage results, automatic package deploy each push to master)
* makefile and other sensible files and configuration already present

## To Use:
1. Copy Repo
2. Replace all instances of "python-package-boilerplate" with your package name
3. Replace "healthchecks_manager" folder name with package name. Do search/replace as well.
4. Replace code & tests
5. Ask devops to register project w/ circleci