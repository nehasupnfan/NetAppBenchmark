import sys
import unittest
sys.path.append("./src/")
from master import argParser


class TestArgParser(unittest.TestCase):
    def test_parser(self):
        parser = argParser(['-i', '127.0.0.1', '-p', '8989', '-r', 'report', '-d', './'])
        self.assertTrue(parser.host, '127.0.0.1')