#!/usr/bin/env python
u"""
flask-discoverer
-------------

Flask extension that enables autodiscovery and broadcast of API endpoints
"""
import os
from subprocess import Popen, PIPE

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

if os.path.isfile('requirements.txt'):
    with open('requirements.txt') as f:
        required = f.read().splitlines()

if os.path.isfile('dev-requirements.txt'):
    with open(u'dev-requirements.txt') as f:
        dev_required = f.read().splitlines()


def get_git_version(default=u'v0.0.1'):
    try:
        p = Popen([u'git', u'describe', u'--tags'], stdout=PIPE, stderr=PIPE)
        p.stderr.close()
        line = p.stdout.readlines()[0].decode()
        line = line.strip()
        return line
    except:
        return default


setup(
    name=u'flask-discoverer',
    url=u'http://github.com/adsabs/flask-discoverer/',

    author=u'Vladimir Sudilovsky',
    author_email=u'vsudilovsky@cfa.harvard.edu',
    classifiers=[
        u'Environment :: Web Environment',
        u'Intended Audience :: Developers',
        u'License :: OSI Approved :: MIT License',
        u'Operating System :: OS Independent',
        u'Programming Language :: Python',
        u'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        u'Topic :: Software Development :: Libraries :: Python Modules',
        u'Programming Language :: Python :: 2.7',
        u'Programming Language :: Python :: 3.6',
    ],
    description=u'Flask API autodiscovery',
    include_package_data=True,
    install_requires=required,
    # if you would be using a package instead use packages instead
    # of py_modules:
    # packages=[u'flask_sqlite3'],
    license=u'MIT',
    platforms=u'any',
    py_modules=[u'flask_discoverer'],
    test_suite=u'tests',
    tests_require=dev_required,
    version=get_git_version(default=u'v0.0.1'),
    zip_safe=False,
)
