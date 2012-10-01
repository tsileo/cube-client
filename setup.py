import os
import sys
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "cube-client",
    version = "0.1",
    author = "Thomas Sileo",
    author_email = "thomas.sileo@gmail.com",
    description = "A Python client for Cube: Time Series Data Collection & Analysis",
    license = "MIT",
    keywords = "cube time series",
    url = "https://github.com/tsileo/cube-client",
    py_modules=['cube'],
    long_description= read('README.rst'),
    install_requires=[
        "requests"
        ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Database",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
    ],
    scripts = ["cube.py"],
    zip_safe=False,
)