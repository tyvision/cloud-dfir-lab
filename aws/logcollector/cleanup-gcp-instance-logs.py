#!/usr/bin/env python3
#
# Test with
# ./cleanup-gcp-cloudaudit-logs.py ./tmp/dirty.json .utmp/clean.jsonl
#
#
import ijson.backends.python as ijson
import json
from datetime import datetime
from dateutil import parser

import importlib
lib_utils = importlib.import_module("lib-utils")

# Example log event:
# {
#    "insertId": "1ohjr20fnk1y6r",
#    "jsonPayload": {
#      "event_subtype": "compute.instances.stop",
#      "resource": {
#        "zone": "us-central1-a",
#        "type": "instance",
#        "name": "instance-2",
#        "id": "7552065986277219937"
#      },
#      "event_type": "GCE_OPERATION_DONE",
#      "trace_id": "operation-1596822570678-5ac4d3a1839cb-5079e259-79ad0bd1",
#      "operation": {
#        "zone": "us-central1-a",
#        "id": "1846247692141865668",
#        "name": "operation-1596822570678-5ac4d3a1839cb-5079e259-79ad0bd1",
#        "type": "operation"
#      },
#      "version": "1.2",
#      "event_timestamp_us": "1596822601607594",
#      "actor": {
#        "user": "constantin.fedenko@gmail.com"
#      }
#    },
#    "resource": {
#      "type": "gce_instance",
#      "labels": {
#        "zone": "us-central1-a",
#        "instance_id": "7552065986277219937",
#        "project_id": "cloud-dfir-lab-groupib"
#      }
#    },
#    "timestamp": "2020-08-07T17:50:01.607594Z",
#    "severity": "INFO",
#    "labels": {
#      "compute.googleapis.com/resource_type": "instance",
#      "compute.googleapis.com/resource_name": "instance-2",
#      "compute.googleapis.com/resource_id": "7552065986277219937",
#      "compute.googleapis.com/resource_zone": "us-central1-a"
#    },
#    "logName": "projects/cloud-dfir-lab-groupib/logs/compute.googleapis.com%2Factivity_log",
#    "receiveTimestamp": "2020-08-07T17:50:01.711680112Z"
#  },


def get_parser():
    helptext="""
Clean up GCP instance logs into timesketch format.
target format https://github.com/google/timesketch/blob/master/docs/CreateTimelineFromJSONorCSV.md
"""
    args = [
        "inputfile"
        , "outputfile"
    ]
    return lib_utils.get_parser(helptext, args)

def cleanup_file2file(inpath, outpath):
    with open(inpath, "r") as infile, open(outpath, "w") as outfile:
        events = ijson.items(infile, 'item')
        for e in events:
            clean = {}

            # secondary fields
            clean["insertId"] = e["insertId"]
            if "severity" in e:
                clean["severity"] = e["severity"]

            if "resource" in e:
                clean["resource_type"] = e["resource"]["type"]

            if "jsonPayload" in e:
                if "event_subtype" in e["jsonPayload"]:
                    clean["event_subtype"] = e["jsonPayload"]["event_subtype"]
                if "resource" in e["jsonPayload"]:
                    clean["resource_id"] = e["jsonPayload"]["resource"]["id"]
                    clean["resource_name"] = e["jsonPayload"]["resource"]["name"]
                if "actor" in e["jsonPayload"]:
                    clean["actor"] = e["jsonPayload"]["actor"]

            # Primary fields
            clean["datetime"] = parser.parse(e["timestamp"]).isoformat()
            clean["timestamp_desc"] = "GCP event"
            clean["message"] = "GCP instance operation"

            outfile.write(json.dumps(clean))
            outfile.write("\n")

if __name__ == "__main__":
    args = get_parser().parse_args()
    cleanup_file2file(args.inputfile, args.outputfile)
