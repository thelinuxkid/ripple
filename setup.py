#!/usr/bin/python
from setuptools import setup, find_packages
import os

# Pypi package documentation
root = os.path.dirname(__file__)
path = os.path.join(root, 'README.rst')
with open(path) as fp:
    long_description = fp.read()

setup(
    name='ripple',
    version='0.0.1',
    description='Python client for rippled',
    long_description=long_description,
    author='Andres Buritica',
    author_email='andres@thelinuxkid.com',
    maintainer='Andres Buritica',
    maintainer_email='andres@thelinuxkid.com',
    url='https://github.com/thelinuxkid/ripple',
    license='MIT',
    packages = find_packages(),
    install_requires=[
        'setuptools',
        ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7'
    ],
)
