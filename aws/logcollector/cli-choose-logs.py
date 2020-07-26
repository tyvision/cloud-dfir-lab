#!/usr/bin/env python3
#
# Test with
# ./cli-choose-logs.py -o tmp
#
import boto3
from pprint import pprint

import importlib

list_log_streams = importlib.import_module("list-log-stream")
download_log_stream = importlib.import_module("download-log-stream")

# list_s3_buckets
# download-s3.py

# list_cloudwatch_metrics
# download-cloudwatch.py

lib_utils = importlib.import_module("lib-utils")


def get_parser():
    helptext="Download selected Log Streams with correct time range."
    args = [
        "outdir"
        , "timestart"
        , "timeend"
    ]
    return lib_utils.get_parser(helptext, args)


def get_possible_download_items():
    res = list_log_streams.list_hierarchy()
    count = 0
    valid = []
    for reg, group_dict in res.items():
        for group, stream_list in group_dict.items():
            for stream in stream_list:
                valid.append([" ", count, reg, group, stream])
                count += 1
    return valid

def interactively_get_index(items):
    for item in items:
        print("{:2} {:3} {:20} {:60} {}".format(*item))

    i = lib_utils.read_integer("Enter index of stream to download or 'q' to quit menu: ", 0, len(items)-1)
    if not i:
        return None

    # change status
    items[i][0] = "+"
    return i

def interactively_download_to_file(args, items):
    for item in items:
        print("{:2} {:3} {:20} {:60} {}".format(*item))

    i = lib_utils.read_integer("Enter index of stream to download or 'exit' to quit: ", 0, len(items)-1)
    if not i:
        return -1

    _, _, cur_reg, cur_group, cur_stream = items[i]

    # perform the download
    download_log_stream.download_log_stream_to_file(cur_reg, cur_group, cur_stream, args.timestart, args.timeend, args.outdir)

    # change status
    items[i][0] = "+"
    print("Download done.")
    return 0


def test_interactive_download():
    args = arguments()

    items = [
        [' ', 0, 'us-east-2', '/aws/rds/instance/artem1/postgresql', 'artem1.0'],
        [' ', 1, 'us-east-2', '/aws/rds/instance/artem1/postgresql', 'artem1.0'],
        [' ', 2, 'us-east-2', '/aws/rds/instance/artem1/postgresql', 'artem1.0']
    ]

    while True:
        interactively_download(args, items)


if __name__ == "__main__":
    # test_interactive_download()
    args = get_parser().parse_args()

    items = get_possible_download_items()

    while interactively_download_to_file(args, items) != -1:
        continue

    print("Exit")
