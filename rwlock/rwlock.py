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


###########################################
import logging
from monotonic import monotonic as now
from threading import Thread
from time import sleep

log = logging.getLogger('tester')


def reader(name, lock, initial_time, start_time, running_time,
           expected_start_time):
    diff = (initial_time + start_time) - now()
    sleep(0 if diff < 0 else diff)

    log.debug("%s: read", name)
    lock.acquire_r()
    log.debug("%s: read start", name)
    t = now() - initial_time
    diff = abs(t - expected_start_time)
    success = (diff / expected_start_time) < 0.1
    log.info("success: %s, t=%s, diff=%s", success, t, diff)
    sleep(running_time)
    log.debug("%s: read end", name)
    lock.release_r()


def writer(name, lock, initial_time, start_time, running_time,
           expected_start_time):
    diff = (initial_time + start_time) - now()
    sleep(0 if diff < 0 else diff)
    log.debug("%s: write", name)
    lock.acquire_w()
    log.debug("%s: write start", name)
    t = now() - initial_time
    diff = abs(t - expected_start_time)
    success = (diff / expected_start_time) < 0.1
    log.info("success: %s, t=%s, diff=%s", success, t, diff)
    sleep(running_time)
    log.debug("%s: write end", name)
    lock.release_w()


if __name__ == '__main__':
    LOG_FMT = "%(asctime)s [%(levelname)s] " \
              "%(filename)s:%(lineno)s %(name)s %(funcName)s() : %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=LOG_FMT)

    rwlock = RwLock(write_first=False)
    initial_time = now()
    r1 = Thread(target=reader,
                args=('r1', rwlock, initial_time, 1, 2, 1)).start()
    r2 = Thread(target=reader,
                args=('r2', rwlock, initial_time, 2, 4, 2)).start()
    r3 = Thread(target=reader,
                args=('r3', rwlock, initial_time, 5, 2, 5)).start()
    w1 = Thread(target=writer,
                args=('w1', rwlock, initial_time, 4, 1, 7)).start()

    rwlock = RwLock(write_first=True)
    initial_time = now()
    r1 = Thread(target=reader,
                args=('r1', rwlock, initial_time, 1, 2, 1)).start()
    r2 = Thread(target=reader,
                args=('r2', rwlock, initial_time, 2, 4, 2)).start()
    r3 = Thread(target=reader,
                args=('r3', rwlock, initial_time, 5, 2, 7)).start()
    w1 = Thread(target=writer,
                args=('w1', rwlock, initial_time, 4, 1, 6)).start()
