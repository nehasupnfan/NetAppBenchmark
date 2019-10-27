import sys
import pytest
import unittest
import time
from mock import patch
from multiprocessing import Process, Event
sys.path.append("../src/")
from communicate.communicatemaster import MasterComm
from benchmark.benchmark import *


class TestConvert2Bytes(object):
	@pytest.mark.parametrize("data, expected", [("10MB", 10000000)])
	def test_convert2bytes(self, data, expected):
		sc = Convert2Bytes(data)
		result = sc.convert2bytes()
		assert result == expected


class TestBenchmark(unittest.TestCase):
	#@patch('benchmark.MasterComm.communicate_message')
	@patch('communicate.communicatemaster.MasterComm.communicate_message')
	def test_write_test(self, mock_comm):
		quit = Event()
		sc = Benchmark(chunk_size="10MB",file="neha", file_size="1MB",url= "", path="./")
		proc = Process(
            target=sc,
            args=("This is a string", quit)
        )
		proc.start()
		time.sleep(5)
		quit.set()
		proc.join()
		#assert result == expected
		#self.assertTrue(mock_comm.called)






