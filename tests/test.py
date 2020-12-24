# coding=utf-8

import argparse
import sys

# create the top-level parser
parser = argparse.ArgumentParser(prog="get")
get = parser.add_subparsers(help="system")
get_system = get.add_parser("system")
get_system_status = get_system.add_subparsers(help="system status")
final = get_system_status.add_parser("status")

args = parser.parse_args()
print(args)