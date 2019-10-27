#!/usr/local/bin/python3

"""
    master.py: Script that will do the following:
                a. Log client performance data to a log file.
                b. Log client heartbeats and client messages to a log file
                c.
    Requires	1: Port to run master on
"""
__author__ = "Neha Ghosh"
__copyright__ = "Copyright 2019"
__date__ = "19th October 2019"
__version__ = "1.0.0"

import sys, os, argparse, time

sys.path.append("../")
sys.path.append('../../')
from logger.logger import Logger
from db.db import Database
from operations.operations_server import Start, Shutdown, Metric, Message, Heartbeat
from db.db_operations import Operation
from operations.middleware import *
import argparse
from threading import Thread, Event

try:
    from wsgiref import simple_server
    import falcon
except Exception as e:
    print(str(e) + ". Please install it")
    sys.exit(1)


def argParser(args):
    """
        Parse argument from command line
    """
    parser = argparse.ArgumentParser(description='Master to get data from clients')
    parser.add_argument('-i', '--host', help='Host ip of the machine', required=True)
    parser.add_argument('-p', '--port', help='Port on which master needs to run', required=True)
    parser.add_argument('-r', '--report-file', help='File to write report in', required=True)
    parser.add_argument('-d', '--report-path', help='Path to write report file', required=True)

    args = parser.parse_args(args)
    # argv = {"host": args.host, "port": int(args.port), "report_file": args.report_file, "report_path": args.report_path}
    # return argv
    return args


def shutdown_server(Data, q):
    db = Data('client.db')
    while True:
        if Operation(db).check_heartbeat_metadata():
            q.set()
            break
        else:
            pass


def write_report(db, **kwargs):
    metric_report = db.execute(["SELECT name, disk, AVG(CPU), AVG(memory) from metrics GROUP BY name;"])
    print(metric_report[0])
    if not os.path.exists(kwargs["path"]):
        os.mkdir(kwargs["path"])
    with open(kwargs["path"] + "/" + kwargs["file"], 'a') as f:
        for item in metric_report[0]:
            f.write("%s using disk %s on an average used cpu of %s percent and memory of %s percent \n" % (
            item[0], item[1], item[2], item[3]))


def create():
    master = falcon.API(middleware=Preprocess())
    # master = falcon.API()
    msg = Message()
    metric = Metric()
    shutdown = Shutdown()
    starts = Start()
    heartbeat = Heartbeat()

    master.add_route('/message', msg)
    master.add_route('/metric', metric)
    master.add_route('/shutdown', shutdown)
    master.add_route('/start', starts)
    master.add_route('/heartbeat', heartbeat)
    return master


master = create()


if __name__ == '__main__':
    logger = Logger.__call__("MASTER", "../logs").get_logger()
    argv = argParser(sys.argv[1:])
    logger.info("Service Running on port: " + argv.port)
    db = Database('client.db')
    Operation(db).create_tables("metrics", "heartbeat")
    httpd = simple_server.make_server(argv.host, int(argv.port), master)
    master_process = Thread(target=httpd.serve_forever, name="master_process")
    master_process.start()
    q = Event()
    # checking when to start the polling for shutdown
    while True:
        if Operation(db).check_start_shutdown_polling():
            heartbeat_process = Thread(target=shutdown_server, args=(Database, q), name="heartbeat_process")
            heartbeat_process.daemon = True
            heartbeat_process.start()
            break
        else:
            pass

    while True:
        if q.is_set():
            shut_process = Thread(target=httpd.shutdown(), name="shut_process")
            shut_process.start()
            shut_process.join()
            break
        else:
            pass

    heartbeat_process.join()
    write_report(db, file=argv.report_file, path=argv.report_path)
    logger.info("Shutting down master!")
