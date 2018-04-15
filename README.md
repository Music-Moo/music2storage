# music2storage

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/aa5db476dcf6497eb25b1ef66bf81e40)](https://app.codacy.com/app/Radu-Raicea/music2storage?utm_source=github.com&utm_medium=referral&utm_content=Music-Moo/music2storage&utm_campaign=badger)

Downloads music from a music service and stores it in a cloud or local storage.

Currently the only music service is Youtube and the only storage is Google Drive. Soundcloud and Dropbox are planned to be added soon.

## Install
```
$ pip3 install music2storage
```

## Usage
```
from music2storage import Music2Storage

m2s = Music2Storage()
m2s.connect_drive()
m2s.start_workers(1)

m2s.add_to_queue('https://www.youtube.com/watch?v=DhHGDOgjie4')
```