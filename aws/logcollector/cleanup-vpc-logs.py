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
import re

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
    logline = re.compile(r"""
                        \s*
                        (?P<version>\S+)
                        \s+
                        (?P<accound_id>\S+)
                        \s+
                        (?P<interface_id>\S+)
                        \s+
                        (?P<srcaddr>\S+)
                        \s+
                        (?P<dstaddr>\S+)
                        \s+
                        (?P<srcport>\S+)
                        \s+
                        (?P<dstport>\S+)
                        \s+
                        (?P<protocol>\S+)
                        \s+
                        (?P<packets>\S+)
                        \s+
                        (?P<bytes>\S+)
                        \s+
                        (?P<start>\S+)
                        \s+
                        (?P<end>\S+)
                        \s+
                        (?P<action>\S+)
                        \s+
                        (?P<log_status>\S+)
                        \s*
                        """, re.X)

    with open(inpath, "rb") as infile, open(outpath, "w") as outfile:
        events = ijson.items(infile, 'events.item')
        for e in events:
            clean = {}

            # Secondary fields
            match = logline.match(e["message"])
            if not match:
                print("Line not matched:\n{}\n".format(line))
                continue
            clean["version"] = match.group('version')
            clean["accound_id"] = match.group('accound_id')
            clean["interface_id"] = match.group('interface_id')
            clean["srcaddr"] = match.group('srcaddr')
            clean["dstaddr"] = match.group('dstaddr')
            clean["srcport"] = match.group('srcport')
            clean["dstport"] = match.group('dstport')
            clean["protocol"] = match.group('protocol')
            clean["packets"] = match.group('packets')
            clean["bytes"] = match.group('bytes')
            clean["start"] = datetime.utcfromtimestamp( int(match.group('start')) ).isoformat()
            clean["end"] = datetime.utcfromtimestamp( int(match.group('end')) ).isoformat()
            clean["action"] = match.group('action')
            clean["log_status"] = match.group('log_status')

            # Primary fields
            clean["datetime"] = datetime.utcfromtimestamp( e["timestamp"] / 1000 ).isoformat()
            clean["timestamp_desc"] = "Flow event captured"
            clean["message"] = "Packet from {} to {}".format(clean["srcaddr"], clean["dstaddr"])

            outfile.write(json.dumps(clean))
            outfile.write("\n")


if __name__ == "__main__":
    args = get_parser().parse_args()
    cleanup_file2file(args.inputfile, args.outputfile)
