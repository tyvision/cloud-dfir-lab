#!/usr/bin/env python3
#
# Test with
# ./cleanup-cloudtrail-logs.py ../config/example-logs/aws_cloudtrail.json.gz ./cleanlogs/aws_cloudtrail.jsonl
#
#
import ijson.backends.python as ijson
import json
from datetime import datetime
from pprint import pprint
import gzip
from dateutil import parser

import importlib
lib_utils = importlib.import_module("lib-utils")


# Example cloudtrail log event:
#         {
#             "eventVersion": "1.05",
#             "userIdentity": {
#                 "type": "Root",
#                 "principalId": "173155781878",
#                 "arn": "arn:aws:iam::173155781878:root",
#                 "accountId": "173155781878",
#                 "accessKeyId": "ASIASQUHDRT3MUDSUOE3",
#                 "sessionContext": {
#                     "sessionIssuer": {},
#                     "webIdFederationData": {},
#                     "attributes": {
#                         "mfaAuthenticated": "true",
#                         "creationDate": "2020-07-08T08:41:05Z"
#                     }
#                 }
#             },
#             "eventTime": "2020-07-08T09:09:51Z",
#             "eventSource": "ec2.amazonaws.com",
#             "eventName": "DescribeInstanceStatus",
#             "awsRegion": "us-east-2",
#             "sourceIPAddress": "37.146.75.28",
#             "userAgent": "console.ec2.amazonaws.com",
#             "requestParameters": {
#                 "instancesSet": {},
#                 "filterSet": {},
#                 "includeAllInstances": false
#             },
#             "responseElements": null,
#             "requestID": "a2aa2231-7175-4742-91fa-2ad6ca922cd2",
#             "eventID": "22b703a7-17e5-4999-9488-a40cf88319a1",
#             "eventType": "AwsApiCall",
#             "recipientAccountId": "173155781878"
#         },


def get_parser():
    helptext="""
Morph Cloud trail logs into timesketch format.
into https://github.com/google/timesketch/blob/master/docs/CreateTimelineFromJSONorCSV.md
"""
    args = [
        "inputfile"
        , "outputfile"
    ]
    return lib_utils.get_parser(helptext, args)

def cleanup_file2file(inpath, outpath):
    with gzip.GzipFile(inpath, 'r') as infile, open(outpath, "w") as outfile:
        json_bytes = infile.read()
        json_str = json_bytes.decode('utf-8')

        events = ijson.items(json_str, 'Records.item')
        for e in events:
            clean = {}

            # secondary fields
            clean["requestID"] = e["requestID"]
            clean["eventID"] = e["eventID"]
            clean["eventType"] = e["eventType"]
            clean["eventSource"] = e["eventSource"]
            clean["awsRegion"] = e["awsRegion"]
            clean["sourceIPAddress"] = e["sourceIPAddress"]
            clean["userAgent"] = e["userAgent"]
            clean["userIdentity"] = json.dumps(e["userIdentity"], indent=2)
            clean["requestParameters"] = json.dumps(e["requestParameters"], indent=2)
            # clean["responseElements"] = json.dumps(e["responseElements"], indent=2)

            clean["userIdentityArn"] = e["userIdentity"]["arn"]
            clean["userIdentityArn"] = e["userIdentity"]["arn"]
            clean["userIdentityType"] = e["userIdentity"]["type"]

            # Primary fields
            clean["datetime"] = parser.parse(e["eventTime"]).isoformat()
            clean["timestamp_desc"] = "CloudTrail event"
            clean["message"] = e["eventName"]

            outfile.write(json.dumps(clean))
            outfile.write("\n")


if __name__ == "__main__":
    args = get_parser().parse_args()
    cleanup_file2file(args.inputfile, args.outputfile)
