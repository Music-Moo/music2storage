# music2storage 

[![Build Status](https://travis-ci.org/Music-Moo/music2storage.svg?branch=master)](https://travis-ci.org/Music-Moo/music2storage)
[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/b4afc41854444e89b73d2d39d842cb0f)](https://www.codacy.com/app/Radu-Raicea/music2storage?utm_source=github.com&utm_medium=referral&utm_content=Music-Moo/music2storage&utm_campaign=Badge_Coverage)
[![PyPi Badge](https://img.shields.io/pypi/v/music2storage.svg)](https://pypi.python.org/pypi/music2storage)
[![PyPi Badge](https://img.shields.io/pypi/l/music2storage.svg)](https://pypi.python.org/pypi/music2storage)
[![PyPi Badge](https://img.shields.io/pypi/pyversions/music2storage.svg)](https://pypi.python.org/pypi/music2storage)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/b4afc41854444e89b73d2d39d842cb0f)](https://www.codacy.com/app/Radu-Raicea/music2storage?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Music-Moo/music2storage&amp;utm_campaign=Badge_Grade)

Downloads music from a music service and stores it in a cloud or local storage.

Currently the only music services are Youtube and Soundcloud, and the only storages are Google Drive and Local Storage. Dropbox is planned to be added soon.

## Install
```
$ pip install music2storage
```

## Usage
```
from music2storage import Music2Storage

m2s = Music2Storage()
m2s.use_music_service('youtube')
m2s.use_storage_service('google drive')
m2s.start_workers()

m2s.add_to_queue('https://www.youtube.com/watch?v=DhHGDOgjie4')
```