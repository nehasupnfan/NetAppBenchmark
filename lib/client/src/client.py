#!/usr/local/bin/python3

"""
	client.py: Script that will do the following:
				a. Will write chunks into a file
				b. Will measure CPU and memory when the chunk writing happens
				c. Will provide a heartbeat to the master
	Requires	1: Name of client
				2: Chunk size
				3: Default time to write 1MB chunk? This is so that we can cater to roll-over mechanism
				4: Run time
				5: URL of master
                6: Name of the file
                7: Fize size
                8: Message to write
                9: Disk to test

"""
__author__ = "Neha Ghosh"
__copyright__ = "Copyright 2019"
__date__ = "15th October 2019"
__version__ = "1.0.0"

import argparse
import sys
import time
from datetime import datetime
from multiprocessing import Process, Event
sys.path.append('../../')
from communicate.communicatemaster import MasterComm
from benchmark.benchmark import Benchmark
from benchmark.metric import Metric
from benchmark.heartbeat import Heartbeat
from logger.logger import Logger


def argParser(args):
    """
        Parse argument from command line
    """
    parser = argparse.ArgumentParser(description='Client to measure disk performance')
    parser.add_argument('-n', '--client-name', help='Name of the client')
    parser.add_argument('-c', '--chunk-size', help='Chunk Size to write data file', default="10MB")
    parser.add_argument('-r', '--run-time', help='Run time for which client will run')
    parser.add_argument('-u', '--url', help='Master service URL', required=True)
    parser.add_argument('-f', '--file', help='File to write in', required=True)
    parser.add_argument('-z', '--file-size', help='File size', required=True)
    parser.add_argument('-m', '--message', help='Message to be written in chunks', required=True)
    parser.add_argument('-p', '--disk-path', help='Message to be written in chunks', required=True)
    argv = parser.parse_args(args)
    return argv


if __name__ == "__main__":
    start_time = time.time()
    argv = argParser(sys.argv[1:])

    logger = Logger.__call__("CLIENT", "../logs").get_logger()

    logger.info("Starting %s " % argv.client_name)
    MasterComm().communicate_message(url=argv.url, msg="Starting %s" % argv.client_name, route="start")

    quit = Event()
    data_process = Process(target=Benchmark(chunk_size=argv.chunk_size, url=argv.url, file_size=argv.file_size,
                                            file=argv.file, path=argv.disk_path, name=argv.client_name).write_test,
                           args=(argv.message, quit),
                           name="data_process")
    data_process.daemon = True
    data_process.start()
    data_pid = data_process.pid

    metric_process = Process(
        target=Metric(pid=data_pid, url=argv.url, name=argv.client_name, path=argv.disk_path).measure,
        args=(quit,), name="metric_process")
    metric_process.daemon = True
    metric_process.start()

    heartbeat_process = Process(target=Heartbeat(name=argv.client_name, url=argv.url).send, args=(quit,),
                                name="heartbeat_process")
    heartbeat_process.daemon = True
    heartbeat_process.start()

    while True:
        if int(time.time() - start_time) > int(argv.run_time):
            logger.info("Run time limit reached for %s" % argv.client_name)
            quit.set()
            break

    # Graceful shutdown
    #shut_down_client()
    logger.info("Shutting down %s gracefully" % argv.client_name)

    MasterComm().communicate_message(url=argv.url, msg="Shutting down: %s" % argv.client_name,
                                     value={"name": argv.client_name, "status": "offline",
                                            "heartbeat_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
                                     route="shutdown")
    sys.exit()
