#!/usr/bin/env python3
#
# one template with conditional attribute on button and different button text.
#
# Page with textarea and button, on button press javascript submits request with "s3", "logstream", "metric" as parameter,
# python runs, returns list JSON, javascript displays it
#
# Page to list all log streams
# Page to list all S3 buckets
# Page to list all metrics
#
# This is a different template for submitting
#
# Page with textarea and button, on button press javascript gets textarea content and submits to python backend for download.
# Time is default from year 2000 to year 3000
#
import ijson.backends.python as ijson
from bottle import request, post, get, route, run, template
import json

import os

from pprint import pprint
from datetime import datetime

import importlib

list_log_streams = importlib.import_module("list-log-stream")
list_gcp_buckets = importlib.import_module("list-gcp-buckets")
# list_log_streams = importlib.import_module("list-log-stream")
# list_log_streams = importlib.import_module("list-log-stream")
transfer_events = importlib.import_module("transfer-events")

aws_id = None
aws_secret = None
gcp_secret_json = None


@get('/display/<storage>')
def storage(storage):
    if not storage in ["s3", "logstream", "cloudwatch", "gcp-bucket"]:
        print("Invalid storage: {}".format(storage))
        return "Invalid storage: {}".format(storage)

    return template("list", storage=storage)

@get('/')
@get('/display/transfer')
def transfer():
    return template("transfer")

@get('/display/settings')
def storage():
    return template("settings")


@get('/action/s3')
def storage_data():
    return 'Not implemented :('

@get('/action/logstream')
def storage_data():
    hierarchy = list_log_streams.list_hierarchy_jsonl(aws_id, aws_secret)
    return hierarchy

@get('/action/cloudwatch')
def storage_data():
    return 'Not implemented :('

@get('/action/gcp-bucket')
def storage_data():
    hierarchy = list_gcp_buckets.list_gcp_buckets_jsonl(gcp_secret_json)
    return hierarchy


@post('/action/settings')
def apply_settings():
    # get parameters
    if request.forms.get('aws_access_key_id'):
        global aws_id
        aws_id = request.forms.get('aws_access_key_id').strip()

    if request.forms.get('aws_secret_access_key'):
        global aws_secret
        aws_secret = request.forms.get('aws_secret_access_key').strip()

    if request.forms.get('gcp_secret_json'):
        global gcp_secret_json
        gcp_secret_json = json.loads( request.forms.get('gcp_secret_json') )

    return '<p>Success!</p>'


@post('/action/transfer')
def post_transfer():
    raw = request.forms.get('transfer_spec')

    targets = list( ijson.items(raw, '', multiple_values=True) )
    timestart = datetime.fromisoformat(request.forms.get('timestart'))
    timeend =   datetime.fromisoformat(request.forms.get('timeend'))

    print(timestart)
    print(timeend)
    pprint(targets)

    # with open("../config/example-transfer-spec.json", "r") as f:
    #     import json
    #     targets = json.load(f)

    # timesketch url is an env variable to make it friendly to docker-compose
    timesketch_url = os.getenv('TIMESKETCH_ADDRESS', "http://localhost:80")

    transfer_events.transfer_events(timesketch_url, targets, timestart, timeend, aws_id=aws_id, aws_secret=aws_secret, gcp_secret_json=gcp_secret_json)
    return "<p>Success!</p>"

port = 9000
print("Running bottle server on port {}".format(port))
run(host='0.0.0.0', port=port, debug=True)
