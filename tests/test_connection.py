# -*- coding: utf-8 -*-

from unittest import TestCase
from unittest.mock import MagicMock, patch

from music2storage.connection import connect_to_drive, connect_to_youtube


class TestConnection(TestCase):
    @patch('music2storage.connection.file.Storage')
    @patch('music2storage.connection.client.flow_from_clientsecrets')
    @patch('music2storage.connection.tools.run_flow')
    @patch('music2storage.connection.build')
    def test_connect_to_drive_creds_invalid_sucess(self, mocked_build, mocked_run, mocked_flow, mocked_storage):
        service = connect_to_drive()
        mocked_storage.assert_called_with('drive_credentials.json')
        self.assertTrue(mocked_storage.return_value.get.called)
        mocked_flow.assert_called_with('client_secret.json', 'https://www.googleapis.com/auth/drive')
        mocked_run.assert_called_with(mocked_flow.return_value, mocked_storage.return_value)
        mocked_build.assert_called_with('drive', 'v3', http=mocked_run.return_value.authorize.return_value)
        self.assertEqual(service, mocked_build.return_value)

    @patch('music2storage.connection.file.Storage')
    @patch('music2storage.connection.build')
    def test_connect_to_drive_creds_valid_sucess(self, mocked_build, mocked_storage):
        mocked_storage.return_value.get.return_value = MagicMock()
        mocked_storage.return_value.get.return_value.invalid = False
        service = connect_to_drive()
        mocked_storage.assert_called_with('drive_credentials.json')
        self.assertTrue(mocked_storage.return_value.get.called)
        mocked_build.assert_called_with('drive', 'v3', http=mocked_storage.return_value.get.return_value.authorize.return_value)
        self.assertEqual(service, mocked_build.return_value)

    @patch('music2storage.connection.file.Storage')
    @patch('music2storage.connection.client.flow_from_clientsecrets')
    @patch('music2storage.connection.tools.run_flow')
    @patch('music2storage.connection.build')
    def test_connect_to_youtube_creds_invalid_sucess(self, mocked_build, mocked_run, mocked_flow, mocked_storage):
        service = connect_to_youtube()
        mocked_storage.assert_called_with('youtube_credentials.json')
        self.assertTrue(mocked_storage.return_value.get.called)
        mocked_flow.assert_called_with('client_secret.json', 'https://www.googleapis.com/auth/youtube.force-ssl')
        mocked_run.assert_called_with(mocked_flow.return_value, mocked_storage.return_value)
        mocked_build.assert_called_with('youtube', 'v3', http=mocked_run.return_value.authorize.return_value)
        self.assertEqual(service, mocked_build.return_value)

    @patch('music2storage.connection.file.Storage')
    @patch('music2storage.connection.build')
    def test_connect_to_youtube_creds_valid_sucess(self, mocked_build, mocked_storage):
        mocked_storage.return_value.get.return_value = MagicMock()
        mocked_storage.return_value.get.return_value.invalid = False
        service = connect_to_youtube()
        mocked_storage.assert_called_with('youtube_credentials.json')
        self.assertTrue(mocked_storage.return_value.get.called)
        mocked_build.assert_called_with('youtube', 'v3', http=mocked_storage.return_value.get.return_value.authorize.return_value)
        self.assertEqual(service, mocked_build.return_value)
