# -*- coding: utf-8 -*-

from queue import Queue
import signal
from threading import Event

from music2storage.connection import connect_to_drive, connect_to_youtube
from music2storage.pipeline import download_from_youtube, convert_to_mp3, upload_to_drive, delete_local_file
from music2storage.signalhandler import SignalHandler
from music2storage.worker import Worker


class Music2Storage:
    """Manages workers, queues, services for music2storage."""

    def __init__(self):
        """Initializes all the queues and sets default values for services and workers."""

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

    def add_to_queue(self, url):
        """
        Adds an URL to the download queue.

        :param str url: URL to the music service track
        """

        if self.drive_service not None:
            self.queues['download'].put(url)
        else:
            print('Drive service is not initialized. URL was not added to queue.')

    def connect_drive(self):
        """Opens browser to allow access to the Google Drive service, creates a credentials file, and returns the service instance."""

        self.drive_service = connect_to_drive()

    def connect_youtube(self):
        """Opens browser to allow access to the Youtube service, creates a credentials file, and returns the service instance."""

        self.youtube_service = connect_to_youtube()

    def start_workers(self, workers_per_task):
        """
        Creates and starts the workers, as well as attaching a handler to terminate them gracefully when a SIGINT signal is received.

        :param int workers_per_task: Number of workers to create for each task in the pipeline
        """

        if not workers:
            for _ in range(workers_per_task):
                self.workers.append(Worker(self._download, self.queues['download'], self.queues['convert'], self.stopper))
                self.workers.append(Worker(self._convert, self.queues['convert'], self.queues['upload'], self.stopper))
                self.workers.append(Worker(self._upload, self.queues['upload'], self.queues['delete'], self.stopper))
                self.workers.append(Worker(self._delete, self.queues['delete'], self.queues['done'], self.stopper))

            self.signal_handler = SignalHandler(self.workers, self.stopper)
            signal.signal(signal.SIGINT, self.signal_handler)

            for worker in self.workers:
                worker.start()

    def _download(self, url):
        """
        Downloads the file associated with the given URL.

        :param str url: URL of the video/audio file
        :return str: Filename of the file in local storage
        """
        
        return download_from_youtube(url)

    def _convert(self, file_name):
        """
        Converts the file associated with the file_name passed into a MP3 file.

        :param str file_name: Filename and extension of the file to be converted
        :return str: Filename of the new file in local storage
        """

        return convert_to_mp3(file_name, self.queues['delete'])

    def _upload(self, file_name):
        """
        Uploads the file associated with the file_name passed to the drive service.

        :param str file_name: Filename of the file to be uploaded
        :return str: Original filename passed as an argument
        """

        return upload_to_drive(self.drive_service, file_name)

    def _delete(self, file_name):
        """
        Deletes the file associated with the file_name passed from local storage.

        :param str file_name: Filename of the file to be deleted
        :return str: Filename of the file that was just deleted
        """

        return delete_local_file(file_name)

    def _notify(self):
        """TODO: Notify that the MP3 has been uploaded through a messaging service."""
        pass
