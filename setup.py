"""A setuptools based setup module for dev-work-tracker"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from codecs import open
from os import path
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))


try:
    import pypandoc
    readme = pypandoc.convert(path.join(here, 'README.rst'), 'rst')
except(IOError, ImportError):
    readme = open('README.rst').read()


requirements = [
    # TODO: put package requirements here
    'jira',
	'spacy',
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='dev-work-tracker',
    version='1.4.3',
    description="This is to track developers work rate",
    long_description=readme,
	#long_description_content_type='text/markdown',
    author="Jagadeesh Lakshminarasimhan",
    author_email='jagadeeshlaks@gmail.com',
    url='https://github.com/jagadeesh-l/dev-work-tracker',
    packages = find_packages(),
    package_data={},
    data_files=[],
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
		'Programming Language :: Python :: 3.8',
    ],
    tests_require=test_requirements,
)
