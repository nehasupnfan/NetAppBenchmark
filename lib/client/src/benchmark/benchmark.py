import os, time, sys

sys.path.append("../../")
sys.path.append("../../../")
from communicate.communicatemaster import MasterComm
from logger.logger import Logger

logger = Logger.__call__("CLIENT", "../logs").get_logger()


class Convert2Bytes(object):
    def __init__(self, val):
        self.val = val

    def convert2bytes(self):
        Data = self.val
        multi = 1000
        if Data:
            if Data.find("K") != -1:
                Data = Data.replace("KB", "")
                return int(Data) * multi
            elif Data.find("M") != -1:
                Data = Data.replace("MB", "")
                return int(Data) * multi * multi
            elif Data.find("B") != -1:
                Data = Data.replace("B", "")
                return int(Data)
        else:
            return 0


class Benchmark:
    def __init__(self, **kwargs):

        self.chunk_size = kwargs["chunk_size"]
        self.file = kwargs["file"]
        self.file_size = kwargs["file_size"]
        self.url = kwargs["url"]
        self.disk_path = kwargs["path"]
        self.name = kwargs["name"]

    def get_currentime(self):
        timestr = time.strftime("%Y%m%d-%H%M%S")
        return timestr

    def chunks(self, lst, n):
        "Yield successive n-sized chunks from lst"
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    def write_test(self, message, quit):
        chunk_size = Convert2Bytes(self.chunk_size).convert2bytes()
        file_size_bytes = Convert2Bytes(self.file_size).convert2bytes()
        indX = 0
        file_name = self.file + '_' + self.get_currentime() + '_' + str(indX) + ".txt"

        if not os.path.exists(self.disk_path):
            os.mkdir(self.disk_path)

        while not quit.is_set():
            with open(self.disk_path + "/" + file_name, "a") as fd:
                for chunk in self.chunks(message, chunk_size):
                    fd.write(chunk)
                    if os.stat(self.disk_path + "/" + file_name).st_size > file_size_bytes:
                        indX += 1
                        file_name = self.file + '_' + self.get_currentime() + '_' + str(indX) + ".txt"
                        logger.info("%s: Rolling over to %s" % (self.name, file_name))
                        MasterComm().communicate_message(url=self.url,
                                                         msg="%s: Reached chunk limit for %s" % (self.name, file_name),
                                                         route="message")
                        # file_name = self.file + str(indX) + ".txt"
                        MasterComm().communicate_message(url=self.url,
                                                         msg="%s: Rolling over to %s" % (self.name, file_name),
                                                         route="message")
        if indX < 1:
            logger.error("%s: Not enough roll overs occurred to benchmark adequately" % self.name)
