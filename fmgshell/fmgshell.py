# coding= utf-8
"""fmgshell: a shell to operate FortiManager."""

import argparse
import getpass

import cmd2

from fmg import FMG
from fmgjsonrpcapi import FMGJSONRPCAPI
from fmgshell_helpers import fmg_print_get_system_status

FMGSHELL_HISTORY_FILE = ".fmgshell_history"


class FMGShell(cmd2.Cmd):
    """Sub-class of the cmd2.Cmd."""

    def __init__(self):
        self.prompt = "fmgshell> "
        self.continuation_prompt = "> "
        self.api = FMGJSONRPCAPI()
        self.logged_in = False
        self.fmg = FMG()
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

        self.api.login(fmg_ip, fmg_username, fmg_password, fmg_port)
        self.logged_in = True

    # Logout from FMG
    def do_logout(self, args):
        """Logout from FortiManager."""
        if self.logged_in:
            self.api.logout()
            self.logged_in = False
        else:
            self.poutput("Not logged in.")

    # Turn on/off debug mode
    debug_parser = argparse.ArgumentParser()
    debug_parser.add_argument(
        "mode", default="show", choices=["on", "off", "show"], help="Turn on debug mode"
    )

    @cmd2.with_argparser(debug_parser)
    def do_debug(self, args):
        """Turn on/off debug mode."""
        if args.mode == "on":
            self.api.debug("on")
        if args.mode == "off":
            self.api.debug("off")
        if args.mode == "show":
            mode = self.api.debug()
            self.poutput(f"Debug is {mode}.")

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
                response = self.fmg.get_system_status(
                    self.api, force_refresh=args.refresh
                )
                self.poutput(fmg_print_get_system_status(response))
        else:
            self.poutput("You need to login first.")
