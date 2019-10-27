import sys
import json
sys.path.append("../")
sys.path.append("../../")
sys.path.append("../../../")
from logger.logger import Logger
from db.db import Database
from db.db_operations import Operation
db = Database('client.db', '')


logger = Logger.__call__("MASTER", "../logs").get_logger()


class CallLogic(object):
    def __init__(self, input_stream):
        self.input_stream = input_stream

    def heartbeat_post(self):
        try:
            req_body = self.input_stream
            json_body = json.loads(req_body.decode('utf-8'))
            json_value = json.loads(json_body["value"].replace("'", '"'))
            logger.info(json_body["heartbeat"])
            Operation(db).check_exists_update(table="heartbeat", column="name", item=json_value["name"],
                                              value=json_value, update_value=[json_value["heartbeat_time"]],
                                              update_column=["heartbeat_time"], where_column="name",
                                              where_clause=json_value["name"])
            response_text = {"result": "success", "message": "Heartbeat registered successfully in Master"}
        except Exception as error:
            response_text = {"result": "error", "message": "Unable to register heartbeat in Master", "error": error}
        return response_text

    def start_post(self):
        try:
            req_body = self.input_stream
            json_body = json.loads(req_body.decode('utf-8'))
            logger.info(json_body["start"])
            response_text = {"result": "success", "message": "Message received successfully"}
        except Exception as error:
            response_text = {"result": "error", "message": "Unable to register message in Master", "error": error}
            # response_json = json.dumps(response_text)
        return response_text

    def shutdown_post(self):
        try:
            req_body = self.input_stream
            json_body = json.loads(req_body.decode('utf-8'))
            logger.info(json_body["shutdown"])
            json_value = json.loads(json_body["value"].replace("'", '"'))
            Operation(db).check_exists_update(table="heartbeat", column="name", item=json_value["name"],
                                              value=json_value,
                                              update_value=[json_value["heartbeat_time"], json_value["status"]],
                                              update_column=["heartbeat_time", "status"], where_column="name",
                                              where_clause=json_value["name"])
            response_text = {"result": "success", "message": "Shutdown message received successfully"}
        except Exception as error:
            response_text = {"result": "error", "message": "Unable to register shutdown in Master", "error": error}
        return response_text

    def metric_post(self):
        try:
            req_body = self.input_stream
            json_body = json.loads(req_body.decode('utf-8'))
            logger.info(json_body["metric"])
            json_value = json.loads(json_body["value"].replace("'", '"'))
            Operation(db).insert_metric(value=json_value, table="metrics")
            response_text = {"result": "success", "message": "Metric received successfully"}
        except Exception as error:
            response_text = {"result": "error", "message": "Unable to register metrics in Master", "error": error}
        return response_text

    def message_post(self):
        try:
            req_body = self.input_stream
            json_body = json.loads(req_body.decode('utf-8'))
            logger.info(json_body["message"])
            response_text = {"result": "success", "message": "Message received successfully"}
        except Exception as error:
            response_text = {"result": "error", "message": "Unable to register message in Master", "error": error}
        return response_text
