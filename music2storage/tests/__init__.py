# -*- coding: utf-8 -*-

import queue
from unittest import TestCase
from unittest.mock import MagicMock, patch

from music2storage import Music2Storage


class TestMusic2Storage(TestCase):
    def test_add_to_queue_with_drive_service(self):
        m2s = Music2Storage()
        m2s.drive_service = MagicMock()
        m2s.add_to_queue('http://example.com/')
        self.assertEqual(m2s.queues['download'].qsize(), 1)
        self.assertEqual(m2s.queues['download'].get_nowait(), 'http://example.com/')

    def test_add_to_queue_without_drive_service(self):
        m2s = Music2Storage()
        m2s.add_to_queue('http://example.com/')
        self.assertEqual(m2s.queues['download'].qsize(), 0)
        with self.assertRaises(queue.Empty):
            m2s.queues['download'].get_nowait()

    @patch('music2storage.connect_to_drive', return_value=MagicMock())
    def test_connect_drive_success(self, mocked_connect_to_drive):
        m2s = Music2Storage()
        m2s.connect_drive()
        self.assertTrue(mocked_connect_to_drive.called)
        self.assertEqual(m2s.drive_service, mocked_connect_to_drive.return_value)

    @patch('music2storage.connect_to_youtube', return_value=MagicMock())
    def test_connect_youtube_success(self, mocked_connect_to_youtube):
        m2s = Music2Storage()
        m2s.connect_youtube()
        self.assertTrue(mocked_connect_to_youtube.called)
        self.assertEqual(m2s.youtube_service, mocked_connect_to_youtube.return_value)

    @patch('music2storage.Worker')
    @patch('music2storage.SignalHandler')
    @patch('music2storage.signal.signal')
    @patch('music2storage.signal.SIGINT')
    def test_start_workers_sucess(self, mocked_signal_sigint, mocked_signal_signal, mocked_signal_handler, mocked_worker):
        m2s = Music2Storage()
        num_of_queues = len(m2s.queues.items())
        m2s.start_workers(2)
        self.assertEqual(len(m2s.workers), num_of_queues*2 - 2)
        self.assertEqual(len(mocked_worker.mock_calls), 2*(num_of_queues*2 - 2))
        self.assertTrue(mocked_signal_handler)
        mocked_signal_handler.assert_called_with(m2s.workers, m2s.stopper)
        mocked_signal_signal.assert_called_with(mocked_signal_sigint, mocked_signal_handler.return_value)
        self.assertEqual(len(mocked_worker.return_value.start.mock_calls), num_of_queues*2 - 2)

    @patch('music2storage.Worker')
    @patch('music2storage.SignalHandler')
    def test_start_workers_already_started(self, mocked_signal_handler, mocked_worker):
        m2s = Music2Storage()
        m2s.workers.append(MagicMock())
        m2s.start_workers(1)
        self.assertEqual(len(m2s.workers), 1)
        self.assertFalse(mocked_worker.called)
        self.assertFalse(mocked_signal_handler.called)
        self.assertFalse(mocked_worker.return_value.start.called)

    @patch('music2storage.download_from_youtube', return_value='filename.mp4')
    def test_download_sucess(self, mocked_download_from_youtube):
        m2s = Music2Storage()
        result = m2s._download('http://example.com/')
        mocked_download_from_youtube.assert_called_with('http://example.com/')
        self.assertEqual(result, 'filename.mp4')

    @patch('music2storage.convert_to_mp3', return_value='filename.mp3')
    def test_convert_sucess(self, mocked_convert_to_mp3):
        m2s = Music2Storage()
        result = m2s._convert('filename.mp4')
        mocked_convert_to_mp3.assert_called_with('filename.mp4', m2s.queues['delete'])
        self.assertEqual(result, 'filename.mp3')

    @patch('music2storage.upload_to_drive', return_value='filename.mp3')
    def test_upload_sucess(self, mocked_upload_to_drive):
        m2s = Music2Storage()
        m2s.drive_service = MagicMock()
        result = m2s._upload('filename.mp3')
        mocked_upload_to_drive.assert_called_with(m2s.drive_service, 'filename.mp3')
        self.assertEqual(result, 'filename.mp3')

    @patch('music2storage.delete_local_file', return_value='filename.mp3')
    def test_delete_sucess(self, mocked_delete_local_file):
        m2s = Music2Storage()
        result = m2s._delete('filename.mp3')
        mocked_delete_local_file.assert_called_with('filename.mp3')
        self.assertEqual(result, 'filename.mp3')
