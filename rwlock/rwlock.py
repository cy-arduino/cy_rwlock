from threading import Lock
# from contextlib import contextmanager


# RwLock: Reader-Writer lock
#
# We can simply protect a shared resource by a lock. But the performance is not
# good because each reader should done one-by-one.
#
# A Reader-Writer lock can improve the performance by
#   1. Let readers running simultaneously
#   2. Exclude "multiple readers" and each writer
#
# By the way, a writer should wait until all reader done.
# In a frequently read situation, a reader after the writer can also increase
# the read count, let read count never decrease to 0. This will starve writer.
# So RwLock provide a flag "write_first" to block the newer read until the
# writer finish it's work.
class RwLock:
    def __init__(self, write_first=True):
        self._write_first = write_first

        self._write_lock = Lock()
        if self._write_first:
            self._read_lock = Lock()  # prevent writer starvation. block new read when someone want to write.
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
