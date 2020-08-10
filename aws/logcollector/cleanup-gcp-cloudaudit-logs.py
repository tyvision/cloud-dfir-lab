#!/usr/bin/env python3
#
# Test with
# ./cleanup-gcp-cloudaudit-logs.py ./tmp/dirty.json .utmp/clean.jsonl
#
#
import ijson.backends.python as ijson
import json
from datetime import datetime

import importlib
lib_utils = importlib.import_module("lib-utils")

# Example log event:
# {
#     "insertId": "12kizl6d97hx",
#     "logName": "projects/cloud-dfir-lab-groupib/logs/cloudaudit.googleapis.com%2Factivity",
#     "operation": {
#         "first": true,
#         "id": "operation-1594396544137-1d558f93",
#         "producer": "container.googleapis.com"
#     },
#     "protoPayload": {
#         "@type": "type.googleapis.com/google.cloud.audit.AuditLog",
#         "authenticationInfo": {
#             "principalEmail": "tykushin@group-ib.com"
#         },
#         "authorizationInfo": [
#             {
#                 "granted": true,
#                 "permission": "container.clusters.delete",
#                 "resourceAttributes": {}
#             }
#         ],
#         "methodName": "google.container.v1.ClusterManager.DeleteCluster",
#         "request": {
#             "@type": "type.googleapis.com/google.container.v1alpha1.DeleteClusterRequest",
#             "name": "projects/cloud-dfir-lab-groupib/locations/us-central1-c/clusters/cluster-1"
#         },
#         "requestMetadata": {
#             "callerIp": "37.16.83.2",
#             "callerSuppliedUserAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36,gzip(gfe)",
#             "destinationAttributes": {},
#             "requestAttributes": {
#                 "auth": {},
#                 "reason": "8uSywAY4GjZGb3IgYmFja2dyb3VuZCBvcGVyYXRpb25zIGluIEdvb2dsZSBEZXZlbG9wZXJzIENvbnNvbGU",
#                 "time": "2020-07-10T15:55:43.98160619Z"
#             }
#         },
#         "resourceLocation": {
#             "currentLocations": [
#                 "us-central1-c"
#             ]
#         },
#         "resourceName": "projects/cloud-dfir-lab-groupib/zones/us-central1-c/clusters/cluster-1",
#         "response": {
#             "@type": "type.googleapis.com/google.container.v1alpha1.Operation",
#             "name": "operation-1594396544137-1d558f93",
#             "operationType": "DELETE_CLUSTER",
#             "selfLink": "https://container.googleapis.com/v1alpha1/projects/746960230895/zones/us-central1-c/operations/operation-1594396544137-1d558f93",
#             "startTime": "2020-07-10T15:55:44.1376654Z",
#             "status": "RUNNING",
#             "targetLink": "https://container.googleapis.com/v1alpha1/projects/746960230895/zones/us-central1-c/clusters/cluster-1"
#         },
#         "serviceName": "container.googleapis.com"
#     },
#     "receiveTimestamp": "2020-07-10T15:55:44.765026895Z",
#     "resource": {
#         "labels": {
#             "cluster_name": "cluster-1",
#             "location": "us-central1-c",
#             "project_id": "cloud-dfir-lab-groupib"
#         },
#         "type": "gke_cluster"
#     },
#     "severity": "NOTICE",
#     "timestamp": "2020-07-10T15:55:44.159104117Z"
#     "timestamp": "2020-07-10T15:55:44.1591Z 04117Z"
# }

def get_parser():
    helptext="""
Clean up GCP cloudaudit logs into timesketch format.
target format https://github.com/google/timesketch/blob/master/docs/CreateTimelineFromJSONorCSV.md
"""
    args = [
        "inputfile"
        , "outputfile"
    ]
    return lib_utils.get_parser(helptext, args)

def cleanup_file2file(inpath, outpath):
    with open(inpath, "r") as infile, open(outpath, "w") as outfile:
        # GCP cloudaudit logs are JSONL
        for line in infile:
            event = json.loads(line)

            clean = {}

            # Secondary fields
            clean["type"] = event["protoPayload"]["@type"]
            if "request" in event["protoPayload"]:
                clean["request"] = event["protoPayload"]["request"]
                clean["requestMetadata"] = event["protoPayload"]["requestMetadata"]
            if "response" in event["protoPayload"]:
                clean["response"] = event["protoPayload"]["response"]
            clean["severity"] = event["severity"]
            clean["resource"] = event["resource"]
            clean["insertId"] = event["insertId"]
            clean["logName"] = event["logName"]
            if "operation" in event:
                clean["operation"] = event["operation"]

            # Primary fields
            # for timestamp, take only first 19 character, thereby dropping milliseconds and time zones
            clean["datetime"] = datetime.fromisoformat( event["timestamp"][:19] ).isoformat()
            clean["message"] = event["protoPayload"]["methodName"]
            clean["timestamp_desc"] = "GPC api event"

            outfile.write(json.dumps(clean))
            outfile.write("\n")


if __name__ == "__main__":
    args = get_parser().parse_args()
    cleanup_file2file(args.inputfile, args.outputfile)
