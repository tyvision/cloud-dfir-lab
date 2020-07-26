#!/usr/bin/env python3
#
# Test with
# ./build-transfer-spec.py
#
#
from pprint import pprint

import importlib
lib_utils = importlib.import_module("lib-utils")
cli_choose_log_stream = importlib.import_module("cli-choose-logs")
transfer_events = importlib.import_module("transfer-events")


def get_parser():
    helptext="""
Interactive menu to build the transfer specification. Use the spec to get events from AWS logs into Timesketch.
"""
    args = []
    return lib_utils.get_parser(helptext, args)

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
            items = cli_choose_log_stream.get_possible_download_items()

            while True:
                item_index = cli_choose_log_stream.interactively_get_index(items)
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
    get_targets()
