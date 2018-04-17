# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
import os
from time import time

from apiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from httplib2 import Http
from oauth2client import file, client, tools
from oauth2client.clientsecrets import InvalidClientSecretsError
from pytube import YouTube
from pytube.exceptions import RegexMatchError


class MusicService(ABC):
    """Template for every music service."""

    @abstractmethod
    def download(self, url):
        """Downloads a song file from the music service."""


class StorageService(ABC):
    """Template for every storage service."""

    @abstractmethod
    def connect(self):
        """Connects to the storage service, sets connection attribute."""

    @abstractmethod
    def upload(self, file_name):
        """Uploads a file to the storage."""


class Youtube(MusicService):
    """Youtube service class."""

    def __init__(self):
        self.name = 'youtube'

    def download(self, url):
        """
        Downloads an MP4 or WebM file that is associated with the video at the URL passed.

        :param str url: URL of the video to be downloaded
        :return str: Filename of the file in local storage
        """

        try:
            yt = YouTube(url)
        except RegexMatchError:
            print(f"Cannot download file at {url}")
        else:
            stream = yt.streams.first()
            print(f"Download for {stream.default_filename} has started")
            start_time = time()
            stream.download()
            end_time = time()
            print(f"Download for {stream.default_filename} has finished in {end_time - start_time} seconds")
            return stream.default_filename


class GoogleDrive(StorageService):
    """Google Drive service class."""

    def __init__(self):
        self.name = 'google drive'
        self.connection = None

    def connect(self):
        """Creates connection to the Google Drive API, sets the connection attribute to make requests, and creates the Music folder if it doesn't exist."""

        SCOPES = 'https://www.googleapis.com/auth/drive'
        store = file.Storage('drive_credentials.json')
        creds = store.get()
        if not creds or creds.invalid:
            try:
                flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
            except InvalidClientSecretsError:
                print('ERROR: Could not find client_secret.json in current directory, please obtain it from the API console.')
                return
            creds = tools.run_flow(flow, store)
        self.connection = build('drive', 'v3', http=creds.authorize(Http()))

        response = self.connection.files().list(q="name='Music' and mimeType='application/vnd.google-apps.folder' and trashed=false").execute()
        try:
            folder_id = response.get('files', [])[0]['id']
        except IndexError:
            print('Music folder is missing. Creating it.')
            folder_metadata = {'name': 'Music', 'mimeType': 'application/vnd.google-apps.folder'}
            folder = self.connection.files().create(body=folder_metadata, fields='id').execute()

    def upload(self, file_name):
        """
        Uploads the file associated with the file_name passed to Google Drive in the Music folder.

        :param str file_name: Filename of the file to be uploaded
        :return str: Original filename passed as an argument (in order for the worker to send it to the delete queue)
        """

        response = self.connection.files().list(q="name='Music' and mimeType='application/vnd.google-apps.folder' and trashed=false").execute()
        folder_id = response.get('files', [])[0]['id']
        file_metadata = {'name': file_name, 'parents': [folder_id]}
        media = MediaFileUpload(file_name, mimetype='audio/mpeg')
        
        print(f"Upload for {file_name} has started")
        start_time = time()
        self.connection.files().create(body=file_metadata, media_body=media, fields='id').execute()
        end_time = time()
        print(f"Upload for {file_name} has finished in {end_time - start_time} seconds")

        return file_name


class LocalStorage(StorageService):
    """Local Storage service class."""

    def __init__(self):
        self.name = 'local'
        self.connection = None

    def connect(self):
        """Initializes the connection attribute with the path to the user home folder's Music folder, and creates it if it doesn't exist."""

        music_folder = os.path.join(os.path.expanduser('~'), 'Music')
        if not os.path.exists(music_folder):
            os.makedirs(music_folder)
        self.connection = music_folder

    def upload(self, file_name):
        """
        Moves the file associated with the file_name passed to the Music folder in the local storage.
        
        :param str file_name: Filename of the file to be uploaded
        """

        print(f"Upload for {file_name} has started")
        start_time = time()
        os.rename(file_name, os.path.join(self.connection, file_name))
        end_time = time()
        print(f"Upload for {file_name} has finished in {end_time - start_time} seconds")
