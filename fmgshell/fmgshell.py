# coding= utf-8
"""fmgshell: a shell to operate FortiManager."""

import argparse
import getpass

import cmd2

from fmg import FMG
from fmgjsonrpcapi import FMGJSONRPCAPI
from fmgshell_helpers import *

FMGSHELL_HISTORY_FILE = ".fmgshell_history"
FMGSHELL_ROOT_DIR = "/"
CMD2_CATEGORY = "fmgshell commands"


class FMGShell(cmd2.Cmd):
    """Sub-class of the cmd2.Cmd."""

    def __init__(self):
        self.prompt = "fmgshell> "
        self.continuation_prompt = "> "
        self.logged_in = False
        self.fmg = FMG()
        self.working_directory = FMGSHELL_ROOT_DIR
        super().__init__(persistent_history_file=FMGSHELL_HISTORY_FILE)

    # Login to FMG
    login_parser = argparse.ArgumentParser()
    login_parser.add_argument(
        "-i", "--ip", required=True, help="FortiManager IP address or FQDN"
    )
    login_parser.add_argument(
        "-u", "--username", required=True, help="FortiManager user name"
    )
    login_parser.add_argument(
        "-p", "--password", required=False, help="FortiManager password"
    )

    login_parser.add_argument("--port", required=False, help="FortiManager TCP port")

    @cmd2.with_argparser(login_parser)
    def do_login(self, args):
        """Login to FortiManager."""
        if self.logged_in:
            self.poutput(f"Already logged in.")
            return

        fmg_ip = args.ip
        fmg_username = args.username
        fmg_password = args.password
        fmg_port = args.port
        if fmg_password == None:
            fmg_password = getpass.getpass()
        if fmg_port == None:
            fmg_port = 443

        self.fmg.login(fmg_ip, fmg_username, fmg_password, fmg_port)
        self.logged_in = True

    cmd2.categorize(do_login, CMD2_CATEGORY)

    # Logout from FMG
    def do_logout(self, args):
        """Logout from FortiManager."""
        if self.logged_in:
            self.fmg.logout()
            self.logged_in = False
        else:
            self.poutput("Not logged in.")

    cmd2.categorize(do_logout, CMD2_CATEGORY)

    # Turn on/off debug mode
    debug_parser = argparse.ArgumentParser()
    debug_parser.add_argument(
        "mode", default="show", choices=["on", "off", "show"], help="Turn on debug mode"
    )

    @cmd2.with_argparser(debug_parser)
    def do_debug(self, args):
        """Turn on/off debug mode."""
        if args.mode == "on":
            self.fmg.debug("on")
        if args.mode == "off":
            self.fmg.debug("off")
        if args.mode == "show":
            mode = self.fmg.debug()
            self.poutput(f"Debug is {mode}.")

    cmd2.categorize(do_debug, CMD2_CATEGORY)

    # "get" command
    get_parser = argparse.ArgumentParser(prog="get")
    # "get system" command
    get_subparser = get_parser.add_subparsers(dest="get_system", required=True)
    get_system = get_subparser.add_parser("system")
    # "get system status" command
    get_system_subparser = get_system.add_subparsers(
        dest="get_system_status", required=True, help="Get FortiManager system status"
    )
    get_system_status = get_system_subparser.add_parser("status")
    get_system_status.add_argument("--refresh", action="store_true")

    @cmd2.with_argparser(get_parser)
    def do_get(self, args):
        """Get information."""
        if self.logged_in:
            # "get system status"
            if args.get_system_status:
                response = self.fmg.get_system_status(force_refresh=args.refresh)
                self.poutput(fmg_print_get_system_status(response))
        else:
            self.poutput("You need to login first.")

    cmd2.categorize(do_get, CMD2_CATEGORY)

    # Print working directory
    def do_pwd(self, args):
        """Print working directory."""
        self.poutput(self.working_directory)

    cmd2.categorize(do_pwd, CMD2_CATEGORY)

    # Change working directory
    def do_cd(self, args):
        """Change working directory."""

        dest_dir = str(args)
        if len(dest_dir) == 0:
            self.working_directory = FMGSHELL_ROOT_DIR
        else:
            self.working_directory = dest_dir

    cmd2.categorize(do_cd, CMD2_CATEGORY)

    def complete_cd(self, text, line, begidx, endidx):

        print(f"\nText: {text}")
        print(f"Line: {line}")
        print(f"Begidx: {begidx}")
        print(f"Endidx: {endidx}\n")
        fs = [
            "/dvmdb/device",
            "/dvmdb/adom",
        ]

        result = cmd2.utils.basic_complete(text, line, begidx, endidx, fs)
        print(f"Result: {result}")
        return result