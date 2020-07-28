#!/usr/bin/env python3
#
# Test with
# ./cleanup-vpc-logs.py ../rawlogs/us-east-2_artem-vpc_eni-049f734adb12b5de9-all.json ../cleanlogs/vpc-clean.jsonl
#
#
import ijson.backends.python as ijson
import json
from datetime import datetime
from pprint import pprint

import importlib
lib_utils = importlib.import_module("lib-utils")

# Example vpc log event:
#     {
#         "timestamp": 1595563795000,
#         "message": "2 173155781878 eni-049f734adb12b5de9 92.63.197.95 10.0.0.249 40378 33992 6 1 40 1595563795 1595563819 REJECT OK",
#         "ingestionTime": 1595563830909
#     },

def get_parser():
    helptext="""
Morph vpc logs into timesketch format.
from https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs.html#flow-logs-default
into https://github.com/google/timesketch/blob/master/docs/CreateTimelineFromJSONorCSV.md
"""
    args = [
        "inputfile"
        , "outputfile"
    ]
    return lib_utils.get_parser(helptext, args)

def cleanup_file2file(inpath, outpath):
    with open(inpath, "rb") as infile, open(outpath, "w") as outfile:
        events = ijson.items(infile, 'events.item')
        for e in events:
            del e["ingestionTime"]

            e["datetime"] = datetime.utcfromtimestamp( e["timestamp"] / 1000 ).isoformat()
            del e["timestamp"]

            e["timestamp_desc"] = "Flow event captured"

            outfile.write(json.dumps(e))
            outfile.write("\n")


if __name__ == "__main__":
    args = get_parser().parse_args()
    cleanup_file2file(args.inputfile, args.outputfile)
