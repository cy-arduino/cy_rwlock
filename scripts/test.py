import os
from unittest import TestLoader, TextTestRunner
import logging

LOG_FMT = "%(asctime)s [%(levelname)s] " \
              "%(filename)s:%(lineno)s %(name)s %(funcName)s() : %(message)s"
logging.basicConfig(level=logging.DEBUG, format=LOG_FMT)

working_path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
tests = TestLoader().discover(working_path, pattern='test*.py')

result = TextTestRunner().run(tests)
