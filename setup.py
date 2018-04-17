# -*- coding: utf-8 -*-

from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='music2storage',
      version='0.1.5',
      description='Downloads music from a service and stores it in a cloud or local storage.',
      long_description='Currently the only music service is Youtube and the only storage is Google Drive. Soundcloud and Dropbox are planned to be added soon.',
      url='https://github.com/Music-Moo/music2storage',
      author='Radu Raicea',
      author_email='radu@raicea.com',
      license='GPLv3',
      packages=['music2storage'],
      install_requires=[
          'ffmpy',
          'google-api-python-client',
          'pytube'
      ],
      include_package_data=True,
      python_requires=">=3.6",
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['nose'])
