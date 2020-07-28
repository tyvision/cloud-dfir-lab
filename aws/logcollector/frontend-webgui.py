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
from bottle import request, post, get, route, run, template
import json

import os

from pprint import pprint
from datetime import datetime

import importlib

list_log_streams = importlib.import_module("list-log-stream")
# list_log_streams = importlib.import_module("list-log-stream")
# list_log_streams = importlib.import_module("list-log-stream")
transfer_events = importlib.import_module("transfer-events")


@get('/display/<storage>')
def storage(storage):
    if not storage in ["s3", "logstream", "cloudwatch"]:
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
    hierarchy = list_log_streams.list_hierarchy()
    return json.dumps(hierarchy, indent=4, sort_keys=True)

@get('/action/cloudwatch')
def storage_data():
    return 'Not implemented :('

@post('/action/settings')
def apply_settings():
    # get parameters
    aws_access_key_id = request.forms.get('aws_access_key_id').strip()
    aws_secret_access_key = request.forms.get('aws_secret_access_key').strip()

    # try setting env variables
    os.environ["AWS_ACCESS_KEY_ID"] = aws_access_key_id
    os.environ["AWS_SECRET_ACCESS_KEY"] = aws_secret_access_key

    return '<p>Success!</p>'

@post('/action/transfer')
def post_transfer():
    targets = json.loads(request.forms.get('transfer_spec'))
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
    aws_id = os.getenv('AWS_ACCESS_KEY_ID', None)
    aws_secret = os.getenv('AWS_SECRET_ACCESS_KEY', None)

    transfer_events.transfer_events(targets, timestart, timeend, timesketch_url)
    return "<p>Success!</p>"

port = 9000
print("Running bottle server on port {}".format(port))
run(host='0.0.0.0', port=port, debug=True)
