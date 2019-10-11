"""A setuptools based setup module for dev-work-tracker"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from codecs import open
from os import path
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

#with open(path.join(here, 'PYPI.md'), encoding='utf-8') as readme_file:
#    readme = readme_file.read()
#readme = readme.replace('\n\n', '\n')

try:
    import pypandoc
    readme = pypandoc.convert(path.join(here, 'PYPI.md'), 'rst')
except(IOError, ImportError):
    readme = open('PYPI.md').read()


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
    version='1.2.0',
    description="This is to track developers work rate",
    long_description=readme,
	#long_description_content_type='text/markdown',
    author="Jagadeesh Lakshminarasimhan",
    author_email='jagadeeshlaks@gmail.com',
    url='https://github.com/jagadeesh-l/dev-work-tracker',
    packages = find_packages(),
    package_data={},
    data_files=[],
    #entry_points={
    #    'console_scripts':[
    #        'dev-work-tracker=dev-work-tracker.cli:cli',
    #        ],
    #    },
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
    ],
    tests_require=test_requirements,
)
