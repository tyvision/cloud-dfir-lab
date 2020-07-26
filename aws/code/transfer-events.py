#!/usr/bin/env python3
#
# Test with
# ./transfer-events.py ../config/example-transfer-spec.json
#
#
import os
import shutil
from pprint import pprint
import json

import importlib
lib_utils = importlib.import_module("lib-utils")

cleanup_vpc_logs = importlib.import_module("cleanup-vpc-logs")
download_log_stream = importlib.import_module("download-log-stream")

cleanup_plugins = {
    "vpc" : cleanup_vpc_logs.cleanup_file2file
    # "cloudtrail" : cleanup_cloudtrail_logs.cleanup_file
}

rawdir = './rawlogs/'
cleandir = "./cleanlogs/"

def get_parser():
    helptext="""
Consumes JSON specification of events to transfer from AWS logs into Timesketch.
See example spec in config/example-transfer-spec.json
"""
    args = [
        "inputfile"
        , "timestart"
        , "timeend"
    ]
    return lib_utils.get_parser(helptext, args)

def recreate_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)

def find_cleanup_plugin(target_info, raw_path):
    return cleanup_plugins.get( target_info["cleanup-plugin"] )

def transfer_events(targets, timestart, timeend, timesketch_url):
    for t in targets["logstream"]:
        region_name = t["region"]
        log_group = t["group"]
        log_stream = t["stream"]

        stream_sane_name = lib_utils.build_sane_basename([region_name, log_group, log_stream])

        raw_path = os.path.join(rawdir, stream_sane_name) + ".json"
        download_log_stream.download_log_stream_to_path(region_name, log_group, log_stream, timestart, timeend, raw_path)

        clean_path = os.path.join(cleandir, stream_sane_name) + ".jsonl"
        cleanup_file2file = find_cleanup_plugin(t, raw_path)
        if cleanup_file2file is None:
            print("Cleanup plugin for {} can not be found, can not upload to timesketch. Skipping this entry.".format(t))
            continue

        cleanup_file2file(raw_path, clean_path)

        command = """timesketch_importer --host '{}' \
                --timeline_name '{}' \
                --sketch_id 1 \
                --username admin \
                --password admin \
                {}
        """.format(timesketch_url, stream_sane_name, clean_path)

        os.system(command)

        print("Done")


if __name__ == "__main__":
    args = get_parser().parse_args()

    recreate_dir(rawdir)
    recreate_dir(cleandir)

    with open(args.inputfile, "r") as f:
        targets = json.load(f)

    transfer_events(targets, args.timestart, args.timeend, "http://localhost:80")
