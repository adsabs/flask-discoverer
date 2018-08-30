#!/usr/bin/env python
"""
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

with open('requirements.txt') as f:
    required = f.read().splitlines()

with open('dev-requirements.txt') as f:
    dev_required = f.read().splitlines()

def get_git_version(default="v0.0.1"):
    try:
        p = Popen(['git', 'describe', '--tags'], stdout=PIPE, stderr=PIPE)
        p.stderr.close()
        line = p.stdout.readlines()[0]
        line = line.strip()
        return line
    except:
        return default


setup(
    name='flask-discoverer',
    version=get_git_version(default="v0.0.1"),
    url='http://github.com/adsabs/flask-discoverer/',
    license='MIT',
    author='Vladimir Sudilovsky',
    author_email='vsudilovsky@cfa.harvard.edu',
    description='Flask API autodiscovery',
    long_description=__doc__,
    py_modules=['flask_discoverer'],
    # if you would be using a package instead use packages instead
    # of py_modules:
    # packages=['flask_sqlite3'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=required,
    test_suite='tests',
    tests_require = dev_required,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
