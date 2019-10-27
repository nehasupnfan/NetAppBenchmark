import sys
# import pytest
import unittest
import json
from mock import patch

sys.path.append("./src/")
from operations.call_logic import CallLogic


class TestCallbacks(unittest.TestCase):
    @patch('db.db_operations.Operation.check_exists_update')
    def test_heartbeat_post(self, mock_dbops):
        input_stream = {"value": {"name": "Client1", "heartbeat_time": "", "status": "alive"},
                        "heartbeat": "Heartbeat Client1 is alive"}
        input_stream = json.dumps(input_stream).encode('utf-8')
        sc = CallLogic(input_stream)
        result = sc.heartbeat_post()
        self.assertTrue(result, {"result": "success", "message": "Heartbeat registered successfully in Master"})

    def test_start_post(self):
        input_stream = {"start": "Starting Client1"}
        input_stream = json.dumps(input_stream).encode('utf-8')
        sc = CallLogic(input_stream)
        result = sc.start_post()
        self.assertTrue(result, {"result": "success", "message": "Message received successfully"})

    @patch('db.db_operations.Operation.check_exists_update')
    def test_shutdown_post(self, mockdbops):
        input_stream = {"value": {"name": "Client1", "heartbeat_time": "", "status": "offline"},
                        "shutdown": "Shutting down: Client1"}
        input_stream = json.dumps(input_stream).encode('utf-8')
        sc = CallLogic(input_stream)
        result = sc.shutdown_post()
        self.assertTrue(result, {"result": "success", "message": "Shutdown message received successfully"})

    @patch('db.db_operations.Operation.check_exists_update')
    def test_metric_post(self, mockdbops):
        input_stream = {"value": {"name": "Client1", "cpu": "0.0", "memory": "4.0", "disk": "./"},
                        "metric": "Metric for Client1 is CPU:: 0.0 , Memory:: 4.0"}
        input_stream = json.dumps(input_stream).encode('utf-8')
        sc = CallLogic(input_stream)
        result = sc.metric_post()
        self.assertTrue(result, {"result": "success", "message": "Metric received successfully"})

    def test_message_post(self):
        input_stream = {"message": "Reached chunk limit for rotate0.txt"}
        input_stream = json.dumps(input_stream).encode('utf-8')
        sc = CallLogic(input_stream)
        result = sc.message_post()
        self.assertTrue(result, {"result": "success", "message": "Message received successfully"})
