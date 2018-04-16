# -*- coding: utf-8 -*-

from queue import Queue
from unittest import TestCase
from unittest.mock import MagicMock, patch, call

from music2storage.pipeline import download_from_youtube, convert_to_mp3, upload_to_drive, delete_local_file
from pytube.exceptions import RegexMatchError


class TestPipeline(TestCase):
    @patch('music2storage.pipeline.YouTube')
    def test_download_from_youtube_bad_link(self, mocked_youtube):
        mocked_youtube.side_effect = RegexMatchError('msg')
        file_name = download_from_youtube('http://example.com/')
        self.assertFalse(mocked_youtube.return_value.streams.first.called)
        self.assertFalse(mocked_youtube.return_value.streams.first.return_value.download.called)
        self.assertIsNone(file_name)

    @patch('music2storage.pipeline.YouTube')
    def test_download_from_youtube_good_link(self, mocked_youtube):
        mocked_youtube.stream.first.return_value.default_filename = 'filename.mp4'
        file_name = download_from_youtube('http://youtube.com/videoid')
        self.assertTrue(mocked_youtube.return_value.streams.first.called)
        self.assertTrue(mocked_youtube.return_value.streams.first.return_value.download.called)
        self.assertEqual(file_name, mocked_youtube.return_value.streams.first.return_value.default_filename)

    @patch('music2storage.pipeline.os.path.splitext', return_value=['filename'])
    @patch('music2storage.pipeline.FFmpeg')
    @patch('music2storage.pipeline.subprocess')
    def test_convert_to_mp3_sucess(self, mocked_subprocess, mocked_ffmpeg, mocked_os):
        delete_queue = Queue()
        file_name = convert_to_mp3('filename.mp4', delete_queue)
        mocked_ffmpeg.assert_called_with(inputs={'filename.mp4': None}, outputs={'filename.mp3': None})
        mocked_ffmpeg.return_value.run.assert_called_with(stdout=mocked_subprocess.DEVNULL, stderr=mocked_subprocess.DEVNULL)
        self.assertEqual(delete_queue.get_nowait(), 'filename.mp4')
        self.assertEqual(file_name, 'filename.mp3')

    @patch('music2storage.pipeline.MediaFileUpload')
    def test_upload_to_drive_music_folder_does_not_exist(self, mocked_mediafileupload):
        mocked_drive_service = MagicMock()
        mocked_files = mocked_drive_service.files.return_value
        mocked_files.list.return_value.execute.return_value = {}
        mocked_files.create.return_value.execute.return_value = {'id': '1'}
        file_name = upload_to_drive(mocked_drive_service, 'filename.mp3')
        mocked_files.list.assert_called_with(q="name='Music' and mimeType='application/vnd.google-apps.folder' and trashed=false")
        mocked_mediafileupload.assert_called_with('filename.mp3', mimetype='audio/mpeg')
        mocked_files.create.assert_has_calls([
            call(body={'name': 'Music', 'mimeType': 'application/vnd.google-apps.folder'}, fields='id'),
            call().execute(),
            call(body={'name': 'filename.mp3', 'parents': ['1']}, media_body=mocked_mediafileupload.return_value, fields='id'),
            call().execute()
        ])
        self.assertEqual(file_name, 'filename.mp3')

    @patch('music2storage.pipeline.MediaFileUpload')
    def test_upload_to_drive_music_folder_exists(self, mocked_mediafileupload):
        mocked_drive_service = MagicMock()
        mocked_files = mocked_drive_service.files.return_value
        mocked_files.list.return_value.execute.return_value = {'files': [{'id': '1'}]}
        file_name = upload_to_drive(mocked_drive_service, 'filename.mp3')
        mocked_files.list.assert_called_with(q="name='Music' and mimeType='application/vnd.google-apps.folder' and trashed=false")
        mocked_mediafileupload.assert_called_with('filename.mp3', mimetype='audio/mpeg')
        mocked_files.create.assert_has_calls([
            call(body={'name': 'filename.mp3', 'parents': ['1']}, media_body=mocked_mediafileupload.return_value, fields='id'),
            call().execute()
        ])
        self.assertEqual(file_name, 'filename.mp3')

    @patch('music2storage.pipeline.os.remove')
    def test_delete_local_file_sucess(self, mocked_remove):
        file_name = delete_local_file('filename.mp3')
        mocked_remove.assert_called_with('filename.mp3')
        self.assertEqual(file_name, 'filename.mp3')

    @patch('music2storage.pipeline.os.remove')
    def test_delete_local_file_oserror(self, mocked_remove):
        mocked_remove.side_effect = OSError()
        file_name = delete_local_file('filename.mp3')
        mocked_remove.assert_called_with('filename.mp3')
        self.assertIsNone(file_name, 'filename.mp3')
