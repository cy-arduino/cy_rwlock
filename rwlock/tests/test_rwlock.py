import logging
import unittest
from threading import Thread
from time import sleep
from unittest import TestCase
from cy_rwlock import RwLock
from time import time as now


class TestRwLock(TestCase):
    def setUp(self):
        if not hasattr(self, 'log'):
            self.log = logging.getLogger(self.__class__.__name__)

    def tearDown(self):
        pass

    def reader(self, name, lock, initial_time, start_time, running_time,
               expected_start_time):
        diff = (initial_time + start_time) - now()
        sleep(0 if diff < 0 else diff)

        self.log.debug("%s: read", name)
        lock.acquire_r()

        self.log.debug("%s: read start", name)
        t = now() - initial_time
        diff = abs(t - expected_start_time)
        success = (diff / expected_start_time) < 0.1
        self.assertTrue(success)
        self.log.info("success: %s, t=%s, diff=%s", success, t, diff)

        sleep(running_time)

        self.log.debug("%s: read end", name)
        lock.release_r()

    def writer(self, name, lock, initial_time, start_time, running_time,
               expected_start_time):
        diff = (initial_time + start_time) - now()
        sleep(0 if diff < 0 else diff)

        self.log.debug("%s: write", name)
        lock.acquire_w()

        self.log.debug("%s: write start", name)
        t = now() - initial_time
        diff = abs(t - expected_start_time)
        success = (diff / expected_start_time) < 0.1
        self.assertTrue(success)
        self.log.info("success: %s, t=%s, diff=%s", success, t, diff)

        sleep(running_time)

        self.log.debug("%s: write end", name)
        lock.release_w()

    def test_rwlock(self):
        rwlock = RwLock(write_first=False)
        threads = []
        initial_time = now()
        threads.append(Thread(target=self.reader,
                              args=('r1', rwlock, initial_time, 1, 2, 1)))
        threads.append(Thread(target=self.reader,
                              args=('r2', rwlock, initial_time, 2, 4, 2)))
        threads.append(Thread(target=self.reader,
                              args=('r3', rwlock, initial_time, 5, 2, 5)))
        threads.append(Thread(target=self.writer,
                              args=('w1', rwlock, initial_time, 4, 1, 7)))
        [t.start() for t in threads]
        [t.join() for t in threads]

    def test_rwlock_write_first(self):
        rwlock = RwLock(write_first=True)
        threads = []
        initial_time = now()
        threads.append(Thread(target=self.reader,
                              args=('r1', rwlock, initial_time, 1, 2, 1)))
        threads.append(Thread(target=self.reader,
                              args=('r2', rwlock, initial_time, 2, 4, 2)))
        threads.append(Thread(target=self.reader,
                              args=('r3', rwlock, initial_time, 5, 2, 7)))
        threads.append(Thread(target=self.writer,
                              args=('w1', rwlock, initial_time, 4, 1, 6)))
        [t.start() for t in threads]
        [t.join() for t in threads]


if __name__ == '__main__':
    LOG_FMT = "%(asctime)s [%(levelname)s] " \
              "%(filename)s:%(lineno)s %(name)s %(funcName)s() : %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=LOG_FMT)
    unittest.main()
