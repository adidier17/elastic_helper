"""A setuptools based setup module.
See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='elastic_helper',  # Required
    version='0.0.1',  # Required
    scripts=['elastic_helper'],
    description='A simple wrapper class for python elasticsearch',  # Optional
    url='https://github.com/adidier17/elastic_helper',  # Optional
    author='Annie Didier',  # Optional
    python_requires='>=3',
    packages=find_packages(),
    install_requires=['elasticsearch==7.0.4'],  # Optional
)
