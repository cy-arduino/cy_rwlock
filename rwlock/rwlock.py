import logging
from contextlib import contextmanager
from multiprocessing import Lock as LockMp
from multiprocessing import Value
from threading import Lock


class RwLock:
    def __init__(self, name=None, write_first=True, debug=False,
                 cross_process=True):
        self.name = name if name else self.__class__.__name__
        self.log = logging.getLogger(self.name)
        self.log.propagate = debug
        self._cross_process = cross_process

        # prevent writer starvation. block new read when someone want to write.
        self._write_first = write_first

        if self._cross_process:
            self._write_lock = LockMp()
            if self._write_first:
                self._read_lock = LockMp()
            self._read_cnt = Value('i', 0)
        else:
            self._write_lock = Lock()
            if self._write_first:
                self._read_lock = Lock()
            self._read_cnt_lock = Lock()
            self._read_cnt = 0

    def acquire_r(self):
        self.log.debug("")
        if self._write_first:
            self.log.debug("wait writter")
            self._read_lock.acquire()
            self.log.debug("wait writter done")
            self._read_lock.release()

        if self._cross_process:
            with self._read_cnt.get_lock():
                self._read_cnt.value += 1
                self.log.debug("read count+ = %s", self._read_cnt.value)
                if self._read_cnt.value == 1:
                    self._write_lock.acquire()
        else:
            with self._read_cnt_lock:
                self._read_cnt += 1
                self.log.debug("read count+ = %s", self._read_cnt)
                if self._read_cnt == 1:
                    self._write_lock.acquire()

    def release_r(self):
        self.log.debug("")
        if self._cross_process:
            with self._read_cnt.get_lock():
                self._read_cnt.value -= 1
                self.log.debug("read count- = %s", self._read_cnt.value)
                if self._read_cnt.value == 0:
                    self._write_lock.release()
        else:
            with self._read_cnt_lock:
                self._read_cnt -= 1
                self.log.debug("read count- = %s", self._read_cnt)
                if self._read_cnt == 0:
                    self._write_lock.release()

    def acquire_w(self):
        self.log.debug("")
        if self._write_first:
            self.log.debug("block new read")
            self._read_lock.acquire()
        self._write_lock.acquire()

    def release_w(self):
        self.log.debug("")
        self._write_lock.release()
        if self._write_first:
            self._read_lock.release()
            self.log.debug("un-block new read")

    @contextmanager
    def lock_r(self):
        try:
            self.acquire_r()
            yield
        finally:
            self.release_r()

    @contextmanager
    def lock_w(self):
        try:
            self.acquire_w()
            yield
        finally:
            self.release_w()
