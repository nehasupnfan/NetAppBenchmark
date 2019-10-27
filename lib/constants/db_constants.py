class Constants:
    metrics = ["name", "cpu", "memory", "disk"]
    heartbeat = ["name", "heartbeat_time", "status"]
    metrics_create = {"name": "TEXT", "cpu": "REAL", "memory": "REAL", "disk": "TEXT"}
    heartbeat_create = {"name": "TEXT", "heartbeat_time" : "DATETIME", "status": "TEXT"}

