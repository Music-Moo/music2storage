# -*- coding: utf-8 -*-

from music2storage import log
from music2storage.service import Youtube, Soundcloud, GoogleDrive, LocalStorage


class ConnectionHandler:
    """Manages all the API connections to the music and storage services."""

    def __init__(self):
        self.current_music = None
        self.current_storage = None
        self.music_services = {}
        self.storage_services = {}

    def use_music_service(self, service_name, api_key):
        """
        Sets the current music service to service_name.

        :param str service_name: Name of the music service
        :param str api_key: Optional API key if necessary
        """

        try:
            self.current_music = self.music_services[service_name]
        except KeyError:
            if service_name == 'youtube':
                self.music_services['youtube'] = Youtube()
                self.current_music = self.music_services['youtube']
            elif service_name == 'soundcloud':
                self.music_services['soundcloud'] = Soundcloud(api_key=api_key)
                self.current_music = self.music_services['soundcloud']
            else:
                log.error('Music service name is not recognized.')

    def use_storage_service(self, service_name, custom_path):
        """
        Sets the current storage service to service_name and runs the connect method on the service.

        :param str service_name: Name of the storage service
        :param str custom_path: Custom path where to download tracks for local storage (optional, and must already exist, use absolute paths only)
        """

        try:
            self.current_storage = self.storage_services[service_name]
        except KeyError:
            if service_name == 'google drive':
                self.storage_services['google drive'] = GoogleDrive()
                self.current_storage = self.storage_services['google drive']
                self.current_storage.connect()
            elif service_name == 'dropbox':
                log.error('Dropbox is not supported yet.')
            elif service_name == 'local':
                self.storage_services['local'] = LocalStorage(custom_path=custom_path)
                self.current_storage = self.storage_services['local']
                self.current_storage.connect()
            else:
                log.error('Storage service name is not recognized.')
