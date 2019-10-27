import sys, time

sys.path.append("../../")
sys.path.append("../../../")
from communicate.communicatemaster import MasterComm
from logger.logger import Logger

# logger = Logger("CLIENT").log('../logs')
logger = Logger.__call__("CLIENT", "../logs").get_logger()
#import psutil
import subprocess


class Metric(object):
    def __init__(self, **kwargs):
        self.pid = kwargs['pid']
        self.interval = 10
        self.url = kwargs["url"]
        self.client_name = kwargs["name"]
        self.disk_path = kwargs["path"]

    def prettify_out(self):
        cmd = "ps -p {0} -o %cpu,%mem".format(self.pid)
        cmd_out = subprocess.Popen([cmd], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        stdout, stderr = cmd_out.communicate()
        s = stdout.decode('utf-8').strip().split()
        return s[-1], s[-2]


    def measure(self, quit):
        while not quit.is_set():
            memory, cpu = self.prettify_out()
            # procs = psutil.Process(self.pid)
            # # procs.cpu_percent
            # c = procs.cpu_percent()
            # memoryUse = (procs.memory_info()[0] / 2. ** 30) / 1000
            metrics = {}
            metrics["cpu"] = cpu
            metrics["memory"] = memory
            metrics["disk"] = self.disk_path
            metrics["name"] = self.client_name
            MasterComm().communicate_message(url=self.url, msg="Metric for %s is CPU:: %s , Memory:: %s" % (
            self.client_name, cpu, memory), route="metric", value=metrics)
            time.sleep(self.interval)
