import logging
from time import sleep
from unittest import TestCase
from rwlock import RwLock
from time import time as now


class TestRwLock(TestCase):
    TIME_ACCURACY = 0.1
    TIME_TICK = 0.1

    def setUp(self):
        if not hasattr(self, 'log'):
            self.log = logging.getLogger(self.__class__.__name__)

    def tearDown(self):
        pass

    def chk_time_match(self, initial_time, expected_start_time):
        t = now() - initial_time
        diff = abs(t - expected_start_time)

        self.log.info("t=%s, diff=%s", t, diff)
        self.assertTrue((diff / expected_start_time) < self.TIME_ACCURACY)

    def reader(self, name, lock, initial_time, start_time, running_time,
               expected_start_time):
        start_time *= self.TIME_TICK
        running_time *= self.TIME_TICK
        expected_start_time *= self.TIME_TICK

        diff = (initial_time + start_time) - now()
        sleep(0 if diff < 0 else diff)

        self.log.debug("%s: in", name)
        with lock.lock_r():
            self.log.debug("%s: start", name)
            self.chk_time_match(initial_time, expected_start_time)
            sleep(running_time)
            self.log.debug("%s: end", name)

    def writer(self, name, lock, initial_time, start_time, running_time,
               expected_start_time):
        start_time *= self.TIME_TICK
        running_time *= self.TIME_TICK
        expected_start_time *= self.TIME_TICK

        diff = (initial_time + start_time) - now()
        sleep(0 if diff < 0 else diff)

        self.log.debug("%s: in", name)
        with lock.lock_w():
            self.log.debug("%s: start", name)
            self.chk_time_match(initial_time, expected_start_time)
            sleep(running_time)
            self.log.debug("%s: end", name)

    def _test_rwlock_write_first(self, cross_process):
        if cross_process:
            from multiprocessing import Process as Runner
        else:
            from threading import Thread as Runner

        rwlock = RwLock(write_first=True, debug=True,
                        cross_process=cross_process)

        runner = []
        initial_time = now()
        runner.append(Runner(target=self.reader,
                             args=('r1', rwlock, initial_time, 1, 2, 1)))
        runner.append(Runner(target=self.reader,
                             args=('r2', rwlock, initial_time, 2, 4, 2)))
        runner.append(Runner(target=self.reader,
                             args=('r3', rwlock, initial_time, 5, 2, 7)))
        runner.append(Runner(target=self.writer,
                             args=('w1', rwlock, initial_time, 4, 1, 6)))
        [w.start() for w in runner]
        [w.join() for w in runner]


    def _test_rwlock(self, cross_process):
        if cross_process:
            from multiprocessing import Process as Runner
        else:
            from threading import Thread as Runner

        self.log.info("cross_process=%s", cross_process)

        rwlock = RwLock(write_first=False, debug=True,
                        cross_process=cross_process)
        runner = []
        initial_time = now()
        runner.append(Runner(target=self.reader,
                             args=('r1', rwlock, initial_time, 1, 2, 1)))
        runner.append(Runner(target=self.reader,
                             args=('r2', rwlock, initial_time, 2, 4, 2)))
        runner.append(Runner(target=self.reader,
                             args=('r3', rwlock, initial_time, 5, 2, 5)))
        runner.append(Runner(target=self.writer,
                             args=('w1', rwlock, initial_time, 4, 1, 7)))
        [w.start() for w in runner]
        [w.join() for w in runner]

    def test_rwlock_process(self):
        self._test_rwlock(cross_process=True)

    def test_rwlock_thread(self):
        self._test_rwlock(cross_process=False)

    def test_rwlock_write_first_process(self):
        self._test_rwlock_write_first(cross_process=True)

    def test_rwlock_write_first_thread(self):
        self._test_rwlock_write_first(cross_process=False)

