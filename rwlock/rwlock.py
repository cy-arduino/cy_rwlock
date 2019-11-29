from threading import Lock
# from contextlib import contextmanager


class RwLock:
    def __init__(self, write_first=True):
        # prevent writer starvation. block new read when someone want to write.
        self._write_first = write_first

        self._write_lock = Lock()
        if self._write_first:
            self._read_lock = Lock()
        self._read_cnt_lock = Lock()
        self._read_cnt = 0

    def acquire_r(self):
        if self._write_first:
            self._read_lock.acquire()
            self._read_lock.release()
        with self._read_cnt_lock:
            self._read_cnt += 1
            if self._read_cnt == 1:
                self._write_lock.acquire()

    def release_r(self):
        with self._read_cnt_lock:
            self._read_cnt -= 1
            if self._read_cnt == 0:
                self._write_lock.release()

    def acquire_w(self):
        if self._write_first:
            self._read_lock.acquire()
        self._write_lock.acquire()

    def release_w(self):
        self._write_lock.release()
        if self._write_first:
            self._read_lock.release()
