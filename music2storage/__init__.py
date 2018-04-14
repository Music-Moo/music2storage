# -*- coding: utf-8 -*-

from queue import Queue
import signal
from threading import Event

from music2storage.connection import connect_to_drive, connect_to_youtube
from music2storage.pipeline import download_from_youtube, convert_to_mp3, upload_to_drive, delete_local_file
from music2storage.signalhandler import SignalHandler
from music2storage.worker import Worker


class Music2Storage:

    def __init__(self):
        self.queues = {
            'download': Queue(),
            'convert': Queue(),
            'upload': Queue(),
            'delete': Queue(),
            'done': Queue(),
        }

        self.drive_service = None
        self.youtube_service = None
        
        self.workers = []
        self.stopper = Event()
        self.signal_handler = None

    def connect_drive(self):
        self.drive_service = connect_to_drive()

    def connect_youtube(self):
        self.youtube_service = connect_to_youtube()

    def start_workers(self, workers_per_task):
        if not workers:

            for _ in range(workers_per_task):
                self.workers.append(Worker(self.download, self.queues['download'], self.queues['convert'], self.stopper))
                self.workers.append(Worker(self.convert, self.queues['convert'], self.queues['upload'], self.stopper))
                self.workers.append(Worker(self.upload, self.queues['upload'], self.queues['delete'], self.stopper))
                self.workers.append(Worker(self.delete, self.queues['delete'], self.queues['done'], self.stopper))

            self.signal_handler = SignalHandler(self.workers, self.stopper)
            signal.signal(signal.SIGINT, self.signal_handler)

            for worker in self.workers:
                worker.start()

    def download(self, url):
        download_from_youtube(url)

    def convert(self, file_name):
        convert_to_mp3(file_name, self.queues['delete'])

    def upload(self, file_name):
        upload_to_drive(self.drive_service, file_name)

    def delete(self, file_name):
        delete_local_file(file_name)

    def notify(self):
        pass
