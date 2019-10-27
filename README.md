# SolidFireNetApp
A benchmarking tool that consists of both a client and a master. The client program measures the performance of locally mounted disks and submits the results back to the server.

## Getting Started

### Prerequisites
This project has dependencies on the below:
```
pip3 install wsgiref
pip3 install falcon
pip3 install pytest
pip3 install pytest-cov
pip3 install pyjwt
```

### How does the tool work?
The master receives messages, heartbeats, metrics from various clients and logs it to its own log file. It maintains the alive/offline status and the metrics coming from clients in an sqlite3 database. After all the clients are finished giving the information, the master writes out a report to a file stating the CPU and memory usage of the clients.

Any request that comes to the master must come with a header token, whose signature the master will verify.

The client, which has a confugured run-time, spawns processes that do the following:
1. Writes to a disk path in chunks and rolls over to a new file once the file reaches its configured size.
2. At 10 second interval it finds out the CPU and memory of the first process and reports to the master
3. At 5 second interval, for the duration of the run time, sends heartbeat to the master.

The client also uses an authorization token to communicate any message to the master over REST.

#### How does the client measure metrics?
The client creates a subprocess shell process that runs the below to get the cpu and memory of the writing process. psutil was not used as it has a dependency on C compiler.
```
P1 = Process(<start the writing/rolling over in the disk process>)
P1_pid = P1.pid

cmd = "ps -p {0} -o %cpu,%mem".format(P1_pid)
subprocess.Popen([cmd],stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
```

### Running the master server
On one terminal session do the below:
```
cd SolidFireNetApp/lib/master/src
python3 master.py -i <ip-of-host> -p <port-to-run-master> -r <name-of-file-to-write-report> -d <dir-to-write-report-in>

Example:
python3 master.py -i 127.0.0.1 -p 8989 -r report.file -d ./
```

### Running the client
On one termimal session do the below:
```
cd SolidFireNetApp/lib/client/src
python3 client.py -n <name-for-client> -c <chunk-size-with-unit> -r <run-time> -u http://<master-host>:<master-port> -z <file-size-with-unit> -f <file-prefix> -m <message-to-write-in-chunks> -p <disk-path-to-benchmark>

Example:
python3 client.py -n Client1 -c 10MB -r 45 -u http://127.0.0.1:8989 -z 1MB -f netapp -m "This is a string" -p /mnt/netapp
```
To start multiple clients, repeat the above step of running the client from different terminals


## Running the unit tests

To get the test coverage of cient
```
cd SolidFireNetApp/lib/client
python3 -m pytest --cov=src tests/
```

```
---------- coverage: platform darwin, python 3.7.4-final-0 -----------
Name                                   Stmts   Miss  Cover
----------------------------------------------------------
src/benchmark/__init__.py                  0      0   100%
src/benchmark/benchmark.py                55     23    58%
src/benchmark/heartbeat.py                20      0   100%
src/benchmark/metric.py                   30      8    73%
src/client.py                             29      0   100%
src/communicate/__init__.py                0      0   100%
src/communicate/communicatemaster.py      19      2    89%
src/conftest.py                            0      0   100%
----------------------------------------------------------
TOTAL                                    153     33    78%


============================ 10 passed in 10.07s ============================
```

To get the test coverage of master
```
cd SolidFireNetApp/lib/master
python3 -m pytest --cov=src tests/
```

```
---------- coverage: platform darwin, python 3.7.4-final-0 -----------
Name                                  Stmts   Miss  Cover
---------------------------------------------------------
src/conftest.py                           0      0   100%
src/master.py                            58     16    72%
src/operations/__init__.py                0      0   100%
src/operations/call_logic.py             64      4    94%
src/operations/middleware.py             14      2    86%
src/operations/operations_server.py      53      5    91%
---------------------------------------------------------
TOTAL                                   189     27    86%
```

## Limitations
The requirement was that if the client run time doesn't allow for at least two file roll overs, then it should complain at the START UP of a client. 
In this code, as the run time limit is reached, and if at least two roll overs have not occured a log is made to the client log stating the below:
```
<Client-Name>: Not enough roll overs occurred to benchmark adequately
```




## Author
Neha Ghosh (neha.spr2005@yahoo.com)

