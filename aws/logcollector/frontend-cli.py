#!/usr/bin/env python3
#
# Test with
# ./main
#
#
import os
import shutil

import importlib
lib_utils = importlib.import_module("lib-utils")

build_transfer_spec = importlib.import_module("build-transfer-spec")
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

def recreate_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)


if __name__ == "__main__":
    args = get_parser().parse_args()

    recreate_dir(rawdir)
    recreate_dir(cleandir)

    targets = build_transfer_spec.get_targets()

    # with open("../config/example-transfer-spec.json", "r") as f:
    #     import json
    #     targets = json.load(f)

    # this is an environment variable to make it friendly to docker-compose
    timesketch_url = os.getenv('TIMESKETCH_ADDRESS', "http://localhost:80")

    transfer_events.transfer_events(targets, args.timestart, args.timeend, timesketch_url)
