#!/usr/bin/env python3.8
import io
from setuptools import setup


setup(
    name='appsync-tools',
    version='2.0.2',
    description='Tools for handling appsync responses and routes.',
    author='Mathew Moon',
    author_email='mmoon@quinovas.com',
    url='https://github.com/QuiNovas/appsync-tools',
    license='Apache 2.0',
    long_description=io.open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    packages=['appsync_tools'],
    package_dir={'appsync_tools': 'src/appsync_tools'},
    install_requires=[],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.8',
    ],
)
