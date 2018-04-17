# -*- coding: utf-8 -*-

import os
import subprocess
from time import time

from ffmpy import FFmpeg, FFRuntimeError

from music2storage import log


def convert_to_mp3(file_name, delete_queue):
    """
    Converts the file associated with the file_name passed into a MP3 file.

    :param str file_name: Filename of the original file in local storage
    :param Queue delete_queue: Delete queue to add the original file to after conversion is done
    :return str: Filename of the new file in local storage
    """


    file = os.path.splitext(file_name)

    if file[1] == '.mp3':
        log.info(f"{file_name} is already a MP3 file, no conversion needed.")
        return file_name

    new_file_name = file[0] + '.mp3'

    ff = FFmpeg(
        inputs={file_name: None},
        outputs={new_file_name: None}
    )

    log.info(f"Conversion for {file_name} has started")
    start_time = time()
    try:
        ff.run(stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FFRuntimeError:
        os.remove(new_file_name)
        ff.run(stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    end_time = time()
    log.info(f"Conversion for {file_name} has finished in {end_time - start_time} seconds")

    delete_queue.put(file_name)
    return new_file_name


def delete_local_file(file_name):
    """
    Deletes the file associated with the file_name passed from local storage.
    
    :param str file_name: Filename of the file to be deleted
    :return str: Filename of the file that was just deleted
    """

    try:
        os.remove(file_name)
        log.info(f"Deletion for {file_name} has finished")
        return file_name
    except OSError:
        pass
