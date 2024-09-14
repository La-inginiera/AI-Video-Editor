import time
import json

processing_status = {"progress": 0}

def status_stream():
    while True:
        time.sleep(1)
        yield f"data: {json.dumps(processing_status)}\n\n"
