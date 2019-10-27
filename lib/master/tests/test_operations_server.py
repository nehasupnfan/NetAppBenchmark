from falcon import testing
import falcon
import pytest
import sys
import json
from mock import patch
sys.path.append("./src/")
from master import create


class TestOpsServer(testing.TestCase):
    def setUp(self):
        super(TestOpsServer, self).setUp()
        self.app = create()


class TestServer(TestOpsServer):
    def test_post_message_negative(self):
        result = self.simulate_post('/message', headers={'token': "xbeybwybewhed"},
                                      body='{"message": "Reached chunk limit for rotate0.txt"}')
        self.assertEqual(result.status_code, 401)

    def test_post_message_positive(self):
        result = self.simulate_post('/message', headers={
            'token': "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.e30.I-MogJLOHysxVlKTIsNLyeKzGMU7AUQ2cxCq4xEg4AU"},
                                      body='{"message": "Reached chunk limit for rotate0.txt"}')
        self.assertEqual(result.status_code, 200)

    @patch('db.db_operations.Operation.check_exists_update')
    def test_post_heartbeat(self, mock_call):
        input_stream = {'value': '{"name": "Client1", "heartbeat_time": "", "status": "alive"}',
                        'heartbeat': 'Heartbeat Client1 is alive'}
        input_stream = json.dumps(input_stream).encode('utf-8')
        result = self.simulate_post('/heartbeat', headers={
            'token': "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.e30.I-MogJLOHysxVlKTIsNLyeKzGMU7AUQ2cxCq4xEg4AU"},
                                      body=input_stream)
        # assert result.json == doc
        assert result.status_code == 200
        assert result.json == {"result": "success", "message": "Heartbeat registered successfully in Master"}

    @patch('db.db_operations.Operation.insert_metric')
    def test_post_metric(self, mock_call):
        input_stream = {'value': '{"name": "Client1", "cpu": "0.0", "memory": "4.0", "disk":"./"}',
                        'metric': 'Metric for %s is CPU:: 0.0 , Memory:: 4.0'}
        input_stream = json.dumps(input_stream).encode('utf-8')
        result = self.simulate_post('/metric', headers={
            'token': "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.e30.I-MogJLOHysxVlKTIsNLyeKzGMU7AUQ2cxCq4xEg4AU"},
                                    body=input_stream)
        assert result.status_code == 200
        assert result.json == {"result": "success", "message": "Metric received successfully"}

    @patch('db.db_operations.Operation.check_exists_update')
    def test_post_shutdown(self, mock_call):
        input_stream = {'value': '{"name": "Client1", "heartbeat_time": "", "status": "offline"}',
                        'shutdown': 'Shutting down: Client1'}
        input_stream = json.dumps(input_stream).encode('utf-8')
        result = self.simulate_post('/shutdown', headers={
            'token': "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.e30.I-MogJLOHysxVlKTIsNLyeKzGMU7AUQ2cxCq4xEg4AU"},
                                    body=input_stream)
        assert result.status_code == 200
        assert result.json == {"result": "success", "message": "Shutdown message received successfully"}

    def test_post_message_start(self):
        result = self.simulate_post('/start', headers={
            'token': "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.e30.I-MogJLOHysxVlKTIsNLyeKzGMU7AUQ2cxCq4xEg4AU"},
                                      body='{"start": "Starting Client1"}')
        self.assertEqual(result.status_code, 200)


