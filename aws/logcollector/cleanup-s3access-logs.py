#!/usr/bin/env python3
#
# Test with
# ./cleanup-s3access-logs.py ../rawlogs/tmp4_AWSLogs_173155781878_CloudTrail_us-east-2_2020_07_21_173155781878_CloudTrail_us-east-2_20200721T1625Z_Edk2rGFweHqgnt9W-json-gz.json ../cleanlogs/s3access-clean.jsonl
#
#
import ijson.backends.python as ijson
import json
from datetime import datetime
from pprint import pprint
from dateutil import parser
import re

import importlib
lib_utils = importlib.import_module("lib-utils")


# Example S3 log event (single line, not json):
#
# 79a59df900b949e55d96a1e698fbacedfd6e09d98eacf8f8d5218e7cd47ef2be awsexamplebucket1 [06/Feb/2019:00:00:38 +0000] 192.0.2.3 79a59df900b949e55d96a1e698fbacedfd6e09d98eacf8f8d5218e7cd47ef2be 3E57427F3EXAMPLE REST.GET.VERSIONING - "GET /awsexamplebucket1?versioning HTTP/1.1" 200 - 113 - 7 - "-" "S3Console/0.4" - s9lzHYrFp76ZVxRcpX9+5cjAnEH2ROuNkd2BHfIa6UkFVdtjf5mKR3/eTPFvsiP/XV/VLi31234= SigV2 ECDHE-RSA-AES128-GCM-SHA256 AuthHeader awsexamplebucket1.s3.us-west-1.amazonaws.com TLSV1.1
#
#
# 79a59df900b949e55d96a1e698fbacedfd6e09d98eacf8f8d5218e7cd47ef2be
# awsexamplebucket1
# [06/Feb/2019:00:00:38 +0000]
# 192.0.2.3
# 79a59df900b949e55d96a1e698fbacedfd6e09d98eacf8f8d5218e7cd47ef2be
# 3E57427F3EXAMPLE
# REST.GET.VERSIONING
# -
# "GET /awsexamplebucket1?versioning HTTP/1.1"
# 200
# -
# 113
# -
# 7
# -
# "-"
# "S3Console/0.4"
# -
# s9lzHYrFp76ZVxRcpX9+5cjAnEH2ROuNkd2BHfIa6UkFVdtjf5mKR3/eTPFvsiP/XV/VLi31234=
# SigV2
# ECDHE-RSA-AES128-GCM-SHA256
# AuthHeader
# awsexamplebucket1.s3.us-west-1.amazonaws.com
# TLSV1.1
#

def get_parser():
    helptext="""
Morph S3 access logs into timesketch format.
from https://docs.aws.amazon.com/AmazonS3/latest/dev/LogFormat.html
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
                        (?P<bucket_owner>\S+)
                        \s+
                        (?P<bucket>\S+)
                        \s+
                        \[              # opening [
                        (?P<time>.*?)   # any character non greedy
                        \]              # closing ]
                        \s+
                        (?P<remote_ip>\S+)
                        \s+
                        (?P<requester>\S+)
                        \s+
                        (?P<request_id>\S+)
                        \s+
                        (?P<operation>\S+)
                        \s+
                        (?P<key>\S+)
                        \s+
                        \"                           # opening "
                        (?P<request_uri>[^"]+?)      # any char except " non greedy
                        \"                           # closing "
                        \s+
                        (?P<http_status>\S+)
                        \s+
                        (?P<error_code>\S+)
                        \s+
                        (?P<bytes_sent>\S+)
                        \s+
                        (?P<object_size>\S+)
                        \s+
                        (?P<total_time>\S+)
                        \s+
                        (?P<turn_around_time>\S+)
                        \s+
                        (?P<referer>\S+)
                        \s+
                        \"                          # opening "
                        (?P<user_agent>[^"]+?)      # any char except " non greedy
                        \"                          # closing "
                        \s+
                        (?P<version_id>\S+)
                        \s+
                        (?P<host_id>\S+)
                        \s+
                        (?P<signature_version>\S+)
                        \s+
                        (?P<cipher_suite>\S+)
                        \s+
                        (?P<authentication_type>\S+)
                        \s+
                        (?P<host_header>\S+)
                        \s+
                        (?P<tls_version>\S+)
                        \s*
                        """, re.X)

    with open(inpath, "r") as infile, open(outpath, "w") as outfile:
        for line in infile:
            match = logline.match(line)
            if not match:
                print("Line not matched:\n{}\n".format(line))
                continue
            clean = {}

            # Secondary fields
            clean["bucket_owner"] = match.group('bucket_owner')
            clean["bucket"] = match.group('bucket')
            clean["time"] = match.group('time')
            clean["remote_ip"] = match.group('remote_ip')
            clean["requester"] = match.group('requester')
            clean["request_id"] = match.group('request_id')
            clean["operation"] = match.group('operation')
            clean["key"] = match.group('key')
            clean["request_uri"] = match.group('request_uri')
            clean["http_status"] = match.group('http_status')
            clean["error_code"] = match.group('error_code')
            clean["bytes_sent"] = match.group('bytes_sent')
            clean["object_size"] = match.group('object_size')
            clean["total_time"] = match.group('total_time')
            clean["turn_around_time"] = match.group('turn_around_time')
            clean["referer"] = match.group('referer')
            clean["user_agent"] = match.group('user_agent')
            clean["version_id"] = match.group('version_id')
            clean["host_id"] = match.group('host_id')
            clean["signature_version"] = match.group('signature_version')
            clean["cipher_suite"] = match.group('cipher_suite')
            clean["authentication_type"] = match.group('authentication_type')
            clean["host_header"] = match.group('host_header')
            clean["tls_version"] = match.group('tls_version')

            # Primary fields
            clean["datetime"] = parser.parse(clean["time"], fuzzy=True).isoformat()
            clean["message"] = "{} for bucket {}".format(clean["operation"], clean["bucket"])
            clean["timestamp_desc"] = "S3 access event"

            outfile.write(json.dumps(clean))
            outfile.write("\n")


if __name__ == "__main__":
    args = get_parser().parse_args()
    cleanup_file2file(args.inputfile, args.outputfile)
