# -*- coding: utf-8 -*-

from unittest import TestCase
from unittest.mock import MagicMock, patch

from music2storage.signalhandler import SignalHandler


class TestSignalHandler(TestCase):
    @patch('music2storage.signalhandler.sys.exit')
    def test_signal_handler_called(self, mocked_exit):
        mocked_workers = [
            MagicMock(),
            MagicMock(),
            MagicMock()
        ]
        mocked_stopper = MagicMock()
        mocked_signum = MagicMock()
        mocked_frame = MagicMock()
        handler = SignalHandler(mocked_workers, mocked_stopper)
        handler(mocked_signum, mocked_frame)
        mocked_stopper.set.assert_called()
        for mocked_worker in mocked_workers:
            mocked_worker.join.assert_called()
        mocked_exit.assert_called_with(0)
