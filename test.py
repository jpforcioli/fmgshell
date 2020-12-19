# coding=utf-8

import argparse
import sys

# create the top-level parser
parser = argparse.ArgumentParser(prog="login")
subparsers = parser.add_subparsers(help="FortiManager connection")

# create the parser for the "ip" command
parser_ip = subparsers.add_parser("ip", help="FortiManager IP")
parser_ip.add_argument("ip", "enter fmg ip")
# create the parser for the "username" command
parser_username = subparsers.add_parser("username", help="FortiManager username")

parser.parse_args(sys.argv[1:])