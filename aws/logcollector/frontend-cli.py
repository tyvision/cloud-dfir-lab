#!/usr/bin/env python3
#
# Test with
# ./main
#
#
import os
import shutil

from pprint import pprint

import importlib
lib_utils = importlib.import_module("lib-utils")
list_log_streams = importlib.import_module("list-log-stream")
transfer_events = importlib.import_module("transfer-events")

rawdir = './rawlogs/'
cleandir = "./cleanlogs/"

def get_parser():
    helptext="""
Interactive menu to choose and transfer events from AWS logs into Timesketch.
"""
    args = [
        "timestart"
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


def get_targets():
    targets = {
        "logstream" : []
        , "s3" : []
        , "metric" : []
    }

    while True:
        print("Choose what type of logs you want to download")
        type_index = lib_utils.read_integer("Choose menu number: 1=log-streams, 2=files in S3, 3=metrics or 'q' to quit menu: ", 1, 3)
        if type_index is None:
            break

        if type_index == 1:
            print("Decide what log stream you want")
            print("Loading list of log streams in AWS...")
            items = get_possible_download_items()

            while True:
                item_index = interactively_get_index(items)
                if item_index is None:
                    break

                while True:
                    plugin_list = list( transfer_events.cleanup_plugins.keys() )
                    message = "Enter cleanup plugin for this log: {} or 'q' to quit menu: ".format(plugin_list)
                    cleanup_plugin_name = lib_utils.read_string(message)
                    if cleanup_plugin_name is None:
                        break
                    if cleanup_plugin_name not in plugin_list:
                        print("Invalid name, choose one of {}".format(plugin_list))
                        continue

                    _, _, cur_reg, cur_group, cur_stream = items[item_index]

                    targets["logstream"].append({
                        "region" : cur_reg
                        , "group" : cur_group
                        , "stream" : cur_stream
                        , "cleanup-plugin" : cleanup_plugin_name
                    })
                    break

        elif type_index == 2:
            print("Decide what S3 paths you want")

        elif type_index == 3:
            print("Decide what cloudwatch metrics you want")

    print("You requested the following logs: ")
    pprint(targets)
    return targets


if __name__ == "__main__":
    args = get_parser().parse_args()
    targets = get_targets()

    # with open("../config/example-transfer-spec.json", "r") as f:
    #     import json
    #     targets = json.load(f)

    # timesketch url is an env variable to make it friendly to docker-compose
    timesketch_url = os.getenv('TIMESKETCH_ADDRESS', "http://localhost:80")
    aws_id = os.getenv('AWS_ACCESS_KEY_ID', None)
    aws_secret = os.getenv('AWS_SECRET_ACCESS_KEY', None)

    transfer_events.transfer_events(targets, args.timestart, args.timeend, timesketch_url, aws_id, aws_secret)
