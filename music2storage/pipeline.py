# -*- coding: utf-8 -*-

import os
import subprocess
from time import time

from ffmpy import FFmpeg
from googleapiclient.http import MediaFileUpload
from pytube import YouTube
from pytube.exceptions import RegexMatchError


def download_from_youtube(url):
    """
    Downloads an MP4 or WebM file that is associated with the video at the URL passed.

    :param str url: URL of the video to be downloaded
    :return str: Filename of the file in local storage
    """

    try:
        yt = YouTube(url)
    except RegexMatchError:
        print(f"Cannot download MP3 at {url}")
    else:
        stream = yt.streams.first()
        print(f"Download for {stream.default_filename} has started")
        start_time = time()
        stream.download()
        end_time = time()
        print(f"Download for {stream.default_filename} has finished in {end_time - start_time} seconds")

        return stream.default_filename


def convert_to_mp3(file_name, delete_queue):
    """
    Converts the file associated with the file_name passed into a MP3 file.

    :param str file_name: Filename of the original file in local storage
    :param Queue delete_queue: Delete queue to add the original file to after conversion is done
    :return str: Filename of the new file in local storage
    """

    new_file_name = os.path.splitext(file_name)[0] + '.mp3'

    ff = FFmpeg(
        inputs={file_name: None},
        outputs={new_file_name: None}
    )

    print(f"Conversion for {file_name} has started")
    start_time = time()
    ff.run(stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    end_time = time()
    print(f"Conversion for {file_name} has finished in {end_time - start_time} seconds")

    delete_queue.put(file_name)
    return new_file_name


def upload_to_drive(drive_service, file_name):
    """
    Uploads the file associated with the file_name passed to Google Drive in the Music folder (creates it in root if it doesn't exist).

    :param Resource drive_service: Google Drive service instance
    :param str file_name: Filename of the file to be uploaded
    :return str: Original filename passed as an argument (in order for the worker to send it to the delete queue)
    """

    response = drive_service.files().list(q="name='Music' and mimeType='application/vnd.google-apps.folder' and trashed=false").execute()

    try:
        folder_id = response.get('files', [])[0]['id']
    except IndexError:
        print('Music folder is missing. Creating it.')
        folder_metadata = {
            'name': 'Music',
            'mimeType': 'application/vnd.google-apps.folder'
        }
        folder = drive_service.files().create(body=folder_metadata, fields='id').execute()
        folder_id = folder.get('id')

    file_metadata = {
        'name': file_name,
        'parents': [folder_id]
    }

    media = MediaFileUpload(file_name, mimetype='audio/mpeg')
    
    print(f"Upload for {file_name} has started")
    start_time = time()
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    end_time = time()
    print(f"Upload for {file_name} has finished in {end_time - start_time} seconds")

    return file_name


def delete_local_file(file_name):
    """
    Deletes the file associated with the file_name passed from local storage.
    
    :param str file_name: Filename of the file to be deleted
    :return str: Filename of the file that was just deleted
    """

    try:
        os.remove(file_name)
        print(f"Deletion for {file_name} has finished")
        return file_name
    except OSError:
        pass
