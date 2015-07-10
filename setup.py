# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import ocl_web
version = ocl_web.__version__

setup(
    name='ocl_web',
    version=version,
    author='',
    author_email='paynejd@gmail.com',
    packages=[
        'ocl_web',
    ],
    include_package_data=True,
    install_requires=[
        'Django>=1.6.1',
    ],
    zip_safe=False,
    scripts=['ocl_web/manage.py'],
)
