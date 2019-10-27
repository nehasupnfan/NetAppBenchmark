import json
import falcon
import sys
from datetime import datetime

sys.path.append("../../../")

from logger.logger import Logger

#from db.db import Database
from operations.call_logic import CallLogic

#db = Database('client.db', '')

logger = Logger.__call__("MASTER", "../logs").get_logger()


class Message(object):
    def on_post(self, req, resp):
        response_text = CallLogic(req.bounded_stream.read()).message_post()
        response_json = json.dumps(response_text)
        resp.body = response_json
        resp.content_type = 'application/json'
        if response_text["result"] == "success":
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_401


class Metric(object):
    def on_post(self, req, resp):
        response_text = CallLogic(req.bounded_stream.read()).metric_post()
        response_json = json.dumps(response_text)
        resp.body = response_json
        resp.content_type = 'application/json'
        if response_text["result"] == "success":
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_401


class Shutdown(object):
    def on_post(self, req, resp):
        response_text = CallLogic(req.bounded_stream.read()).shutdown_post()
        response_json = json.dumps(response_text)
        resp.body = response_json
        resp.content_type = 'application/json'
        if response_text["result"] == "success":
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_401


class Start(object):
    def on_post(self, req, resp):
        response_text = CallLogic(req.bounded_stream.read()).start_post()
        response_json = json.dumps(response_text)
        resp.body = response_json
        resp.content_type = 'application/json'
        if response_text["result"] == "success":
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_401


class Heartbeat(object):
    def on_post(self, req, resp):
        response_text = CallLogic(req.bounded_stream.read()).heartbeat_post()
        response_json = json.dumps(response_text)
        resp.body = response_json
        resp.content_type = 'application/json'
        if response_text["result"] == "success":
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_401

