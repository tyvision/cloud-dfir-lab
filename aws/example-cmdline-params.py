#!/usr/bin/env python3
import argparse

parser = argparse.ArgumentParser(description='Download logs from AWS')

parser.add_argument('log_group', type=str, help='Name of the log-group')
parser.add_argument('log_stream', type=str, help='Name of the log-stream within the log-group')
parser.add_argument('-o', '--outdir', type=str, help='Path to output directory')

args = parser.parse_args()

print(args.log_group)
print(args.log_stream)
print(args.outdir)
