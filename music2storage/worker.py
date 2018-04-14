# -*- coding: utf-8 -*-

import queue
from threading import Thread


class Worker(Thread):
    """Worker that processes items from an input queue and puts the result into an output queue."""

    def __init__(self, func, in_queue, out_queue, stopper):
        """
        Builds a worker by taking a function that does work on items from the input queue to be put in the output queue.

        :param function func: Function that does work on items from the input queue
        :param Queue in_queue: Input queue
        :param Queue out_queue: Output queue
        :param threading.Event stopper: Event that signals that the thread should stop execution
        """
        
        super().__init__()
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.stopper = stopper

    def run(self):
        """
        Method that gets run when the Worker thread is started.

        When there's an item in in_queue, it takes it out, passes it to func as an argument, and puts the result in out_queue.
        """

        while not self.stopper.is_set():
            try:
                item = self.in_queue.get(timeout=5)
            except queue.Empty:
                continue

            try:
                result = self.func(item, service=None)
            except TypeError:
                continue
            else:
                self.out_queue.put(result)
