import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='cube-client',
    version='0.2.0',
    author='Thomas Sileo',
    author_email='thomas.sileo@gmail.com',
    description='A Python client for Cube: Time Series Data Collection & Analysis',
    license='MIT',
    keywords='cube time series',
    url='https://github.com/tsileo/cube-client',
    packages=find_packages(exclude=['ez_setup', 'tests', 'tests.*']),
    test_suite="cube.tests",
    long_description=read('README.rst'),
    install_requires=['requests'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Database',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
    ],
    zip_safe=False,
)
