# A class for a timer
# Got this Snippet from Stockoverflow: https://stackoverflow.com/a/13151299
import os
from threading import Timer


class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False


def getVideoFolderPath(filename=None):
    if filename != None:
        path = os.getcwd()
        path = os.path.join(path, "static")
        path = os.path.join(path, "video")
        path = os.path.join(path, filename)
    else:
        path = os.getcwd()
        path = os.path.join(path, "static")
        path = os.path.join(path, "video")
    return path


def get_next_possible_filename(path, file_ending=""):
    sequence = ""

    while os.path.isfile(path + str(sequence) + file_ending):
        sequence = int(sequence or 0) + 1
    path = path + str(sequence)
    return path + file_ending
