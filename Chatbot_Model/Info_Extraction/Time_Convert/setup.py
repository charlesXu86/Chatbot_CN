#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/5 15:10
# @Author  : zhm
# @File    : setup.py.py
# @Software: PyCharm
# @Changed : tianyuningmou

from setuptools import setup

setup(
    name="TimeConverter",
    version="1.1.0",
    keywords=("time", "nlp"),
    description="...",
    long_description="...",
    license="MIT Licence",
    url="http://test.com",
    author="test",
    author_email="test@gmail.com",
    packages=['', 'resource'],
    package_data={'resource': ['*.json', '*.pkl']},
    include_package_data=True,
    platforms="any",
    install_requires=['regex>=2017',
                      'arrow>=0.10'],
    zip_safe=False,
    classifiers=[
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.6'
        ]
)