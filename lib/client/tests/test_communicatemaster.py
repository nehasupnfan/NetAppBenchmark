from communicate.communicatemaster import MasterComm
import sys
import pytest
import unittest
from mock import patch
from datetime import datetime

sys.path.append("./src/")


def mocked_requests_post(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] == 'http://127.0.0.1:8989/start':
        return MockResponse({"result": "success", "message": "Message received successfully"}, 200).json()
    elif args[0] == 'http://127.0.0.1:8989/shutdown':
        return MockResponse({"result": "success", "message": "Shutdown message received successfully"}, 200).json()
    elif args[0] == 'http://127.0.0.1:8989/message':
        return MockResponse({"result": "success", "message": "Message received successfully"}, 200).json()

    return MockResponse(None, 404)


class TestCommunicateMaster(unittest.TestCase):
    @patch('requests.post', side_effect=mocked_requests_post)
    def test_communicatemessage_start(self, mock_post):
        sc = MasterComm()
        sc.communicate_message(url="http://127.0.0.1:8989", msg="Starting Client", route="start")
        self.assertEqual(len(mock_post.call_args_list), 1)

    @patch('requests.post', side_effect=mocked_requests_post)
    def test_communicatmessage_shutdown(self, mock_post):
        sc = MasterComm()
        sc.communicate_message(url="http://127.0.0.1:8989", msg="Shutting down: Client1",
                               value={"name": "Client1", "status": "offline",
                                      "heartbeat_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
                               route="shutdown")
        self.assertEqual(len(mock_post.call_args_list), 1)

    @patch('requests.post', side_effect=mocked_requests_post)
    def test_communicatmessage_message(self, mock_post):
        sc = MasterComm()
        sc.communicate_message(url="http://127.0.0.1:8989/message", msg="Reached chunk limit for rotate0", route="message")
        self.assertEqual(len(mock_post.call_args_list), 1)
