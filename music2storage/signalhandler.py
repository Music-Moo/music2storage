# -*- coding: utf-8 -*-

import sys

from music2storage import log


class SignalHandler:
    """Handles signals and stops the worker threads."""

    def __init__(self, workers, stopper):
        """
        Creates a SignalHandler associated with all the worker threads and a stopper Event object.

        :param list workers: List of all the worker threads from the Worker class
        :param threading.Event stopper: Event that signals that the thread should stop execution
        """

        self.workers = workers
        self.stopper = stopper

    def __call__(self, signum, frame):
        """
        Gets called by Python's signal module when the threads should be stopped.

        :param signal signum: Signal number that must be handled
        :param Frame frame: Current stack frame
        """

        log.info('Gracefully killing the threads...')
        self.stopper.set()

        for worker in self.workers:
            worker.join(1)

        sys.exit(0)
