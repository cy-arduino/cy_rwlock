import os
from unittest import TestLoader, TextTestRunner

working_path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
tests = TestLoader().discover(working_path, pattern='test*.py')

result = TextTestRunner().run(tests)
