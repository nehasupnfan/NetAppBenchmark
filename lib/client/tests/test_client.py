import sys
import pytest
import unittest
from mock import patch

sys.path.append("./src/")
from client import argParser



class TestArgParser(unittest.TestCase):
    def test_parser(self):
        parser = argParser(
            ['-u', 'http://127.0.0.1:8989', '-z', '1MB', '-f', 'neha', '-m', 'This is a string', '-p', './disk'])
        self.assertTrue(parser.url, 'http://127.0.0.1:8989')

