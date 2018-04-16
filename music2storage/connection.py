# -*- coding: utf-8 -*-

from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools


class ConnectionHandler:
    """Manages all the API connections to the music and storage services."""

    def __init__(self):
        """Sets the default music and storage services to None."""

        self.music_service = None
        self.storage_service = None

    def connect_music_service(self, service_name):
        """
        Creates a connection to the music service with name service_name.

        :param str service_name: Name of the music service
        """

        if service_name == 'youtube':
            self.music_service = self._connect_to_youtube()
        elif service_name == 'soundcloud':
            print('Soundcloud is not supported yet.')
        else:
            print('Music service name is not recognized.')

    def connect_storage_service(self, service_name):
        """
        Creates a connection to the storage service with name service_name.

        :param str service_name: Name of the storage service
        """

        if service_name == 'google drive':
            self.storage_service = self._connect_to_drive()
        elif service_name == 'dropbox':
            print('Dropbox is not supported yet.')
        else:
            print('Storage service name is not recognized.')

    @staticmethod
    def _connect_to_drive():
        """
        Creates connection to the Google Drive API and returns the service object to make requests.

        :return googleapiclient.discovery.Resource:
        """

        SCOPES = 'https://www.googleapis.com/auth/drive'
        store = file.Storage('drive_credentials.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
            creds = tools.run_flow(flow, store)
        service = build('drive', 'v3', http=creds.authorize(Http()))
        return service

    @staticmethod
    def _connect_to_youtube():
        """
        Creates connection to the Youtube API and returns the service object to make requests.

        :return googleapiclient.discovery.Resource:
        """

        SCOPES = 'https://www.googleapis.com/auth/youtube.force-ssl'
        store = file.Storage('youtube_credentials.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
            creds = tools.run_flow(flow, store)
        service = build('youtube', 'v3', http=creds.authorize(Http()))
        return service  
