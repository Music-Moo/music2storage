# -*- coding: utf-8 -*-

import queue
from unittest import TestCase
from unittest.mock import MagicMock

from music2storage.worker import Worker


class TestWorker(TestCase):
    def test_worker_run_success(self):
        mocked_func = MagicMock()
        mocked_func.return_value = 'result'
        mocked_in_queue = MagicMock()
        mocked_in_queue.get.return_value = 'next item'
        mocked_out_queue = MagicMock()
        mocked_stopper = MagicMock()
        mocked_stopper.is_set.side_effect = [False, True]
        worker = Worker(mocked_func, mocked_in_queue, mocked_out_queue, mocked_stopper)
        worker.run()
        mocked_in_queue.get.assert_called_with(timeout=5)
        mocked_func.assert_called_with('next item')
        mocked_out_queue.put.assert_called_with('result')

    def test_worker_run_stopper_is_set(self):
        mocked_func = MagicMock()
        mocked_in_queue = MagicMock()
        mocked_out_queue = MagicMock()
        mocked_stopper = MagicMock()
        mocked_stopper.is_set.return_value = True
        worker = Worker(mocked_func, mocked_in_queue, mocked_out_queue, mocked_stopper)
        worker.run()
        self.assertFalse(mocked_in_queue.get.called)
        self.assertFalse(mocked_func.called)
        self.assertFalse(mocked_out_queue.put.called)

    def test_worker_run_empty_in_queue(self):
        mocked_func = MagicMock()
        mocked_in_queue = MagicMock()
        mocked_in_queue.get.side_effect = queue.Empty()
        mocked_out_queue = MagicMock()
        mocked_stopper = MagicMock()
        mocked_stopper.is_set.side_effect = [False, True]
        worker = Worker(mocked_func, mocked_in_queue, mocked_out_queue, mocked_stopper)
        worker.run()
        mocked_in_queue.get.assert_called_with(timeout=5)
        self.assertFalse(mocked_func.called)
        self.assertFalse(mocked_out_queue.put.called)

    def test_worker_run_type_error(self):
        mocked_func = MagicMock()
        mocked_func.side_effect = TypeError()
        mocked_in_queue = MagicMock()
        mocked_out_queue = MagicMock()
        mocked_stopper = MagicMock()
        mocked_stopper.is_set.side_effect = [False, True]
        worker = Worker(mocked_func, mocked_in_queue, mocked_out_queue, mocked_stopper)
        worker.run()
        mocked_in_queue.get.assert_called_with(timeout=5)
        self.assertTrue(mocked_func.called)
        self.assertFalse(mocked_out_queue.put.called)
