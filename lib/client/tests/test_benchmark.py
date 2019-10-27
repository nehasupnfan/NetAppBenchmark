import sys
import pytest
import unittest
import mock
from multiprocessing import Process, Event
import builtins
sys.path.append("./src/")
from benchmark.benchmark import *
from benchmark.heartbeat import *
from benchmark.metric import *


class TestConvert2Bytes(object):
    @pytest.mark.parametrize("data, expected", [("10MB", 10000000), ("10KB", 10000), ("100B", 100)])
    def test_convert2bytes(self, data, expected):
        sc = Convert2Bytes(data)
        result = sc.convert2bytes()
        assert result == expected


class TestBenchmark(unittest.TestCase):

    @mock.patch('communicate.communicatemaster.MasterComm.communicate_message')
    @mock.patch('os.path.exists')
    @mock.patch('os.mkdir')
    @mock.patch('os.stat')
    def test_write_test(self, mock_os_stat_size, mock_os_mkdir, mock_os_exists, mock_comm):
        mock_os_stat_size.return_value = mock.Mock(st_size=1000000)
        with mock.patch('builtins.open', mock.mock_open()) as m:
            quit = Event()
            sc = Benchmark(chunk_size="10MB", file="rotate", file_size="1MB", url="", path="./", name="Client1").write_test
            #sc = Benchmark(chunk_size="10MB", file="rotate", file_size="1MB", url="", path="./")
            #sc.write_test("This is a string", quit)
            proc = Process(
                target=sc,
                args=("This is a string", quit)
            )
            proc.start()
            time.sleep(2)
            quit.set()
            proc.join()
        # for filename in glob.glob("./rotate*"):
        #     assert os.path.getsize(filename) < 1000000

class TestHeartbeat(unittest.TestCase):
    @mock.patch('communicate.communicatemaster.MasterComm.communicate_message')
    def test_heartbeat(self, mock_comm):
        quit = Event()
        sc = Heartbeat(url="http:127.0.0.1:8989", name="Client1").send
        proc = Process(
            target=sc,
            args=(quit,)
        )
        proc.start()
        time.sleep(5)
        quit.set()
        proc.join()

class TestMetric(unittest.TestCase):
    @mock.patch('communicate.communicatemaster.MasterComm.communicate_message')
    @mock.patch('subprocess.Popen')
    def test_measure(self, mock_subproc_popen, mock_comm):
        quit = Event()
        process_mock = mock.Mock()
        attrs = {'communicate.return_value': ('%CPU %MEM', '88.9  0.1')}
        process_mock.configure_mock(**attrs)
        mock_subproc_popen.return_value = process_mock
        sc = Process(
            target=Metric(pid=9089, url="http:127.0.0.1:8989", name="Client1", path="./").measure,
            args=(quit,)
        )
        sc.start()
        time.sleep(2)
        quit.set()
        sc.join()





