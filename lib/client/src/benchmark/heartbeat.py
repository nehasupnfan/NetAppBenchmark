import sys, time
from datetime import datetime

sys.path.append("../../")
sys.path.append("../../../")
from communicate.communicatemaster import MasterComm
from logger.logger import Logger

logger = Logger.__call__("CLIENT", "../logs").get_logger()


class Heartbeat(object):
    def __init__(self, **kwargs):
        self.interval = 5
        self.url = kwargs["url"]
        self.name = kwargs["name"]

    def send(self, quit):
        while not quit.is_set():
            heartbeat = {}
            heartbeat["name"] = self.name
            heartbeat["heartbeat_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            heartbeat["status"] = "alive"
            MasterComm().communicate_message(url=self.url,
                                             msg="Heartbeat %s is alive" % self.name,
                                             route="heartbeat", value=heartbeat)
            time.sleep(self.interval)
