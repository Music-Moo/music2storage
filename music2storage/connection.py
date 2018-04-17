# -*- coding: utf-8 -*-

from music2storage.service import Youtube, GoogleDrive, LocalStorage


class ConnectionHandler:
    """Manages all the API connections to the music and storage services."""

    def __init__(self):
        self.current_music = None
        self.current_storage = None
        self.music_services = {}
        self.storage_services = {}

    def use_music_service(self, service_name):
        """
        Sets the current music service to service_name.

        :param str service_name: Name of the music service
        """

        try:
            self.current_music = self.music_services[service_name]
        except KeyError:
            if service_name == 'youtube':
                self.music_services['youtube'] = Youtube()
                self.current_music = self.music_services['youtube']
            elif service_name == 'soundcloud':
                print('Soundcloud is not supported yet.')
            else:
                print('Music service name is not recognized.')

    def use_storage_service(self, service_name):
        """
        Sets the current storage service to service_name and runs the connect method on the service.

        :param str service_name: Name of the storage service
        """
        try:
            self.current_storage = self.storage_services[service_name]
        except KeyError:
            if service_name == 'google drive':
                self.storage_services['google drive'] = GoogleDrive()
                self.current_storage = self.storage_services['google drive']
                self.current_storage.connect()
            elif service_name == 'dropbox':
                print('Dropbox is not supported yet.')
            elif service_name == 'local':
                self.storage_services['local'] = LocalStorage()
                self.current_storage = self.storage_services['local']
                self.current_storage.connect()
            else:
                print('Storage service name is not recognized.')
