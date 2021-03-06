# coding= utf-8
"""fmgshell: a shell to operate FortiManager."""

import argparse
import getpass

import cmd2

from fmg import FMG
from fmgfs import *
from fmgjsonrpcapi import FMGJSONRPCAPI
from fmgshell_helpers import *

FMGSHELL_HISTORY_FILE = ".fmgshell_history"
FMGFS_ROOT_DIR = "root"
CMD2_CATEGORY = "fmgshell commands"


class FMGShell(cmd2.Cmd):
    """Sub-class of the cmd2.Cmd."""

    def __init__(self):
        super().__init__(persistent_history_file=FMGSHELL_HISTORY_FILE)

        # The prompt string - Inherited from cmd2.Cmd
        self.prompt = "fmgshell> "

        # Prompt string for multine command - Inherited from cmd2.Cmd
        self.continuation_prompt = "> "

        # A flag set to true once self.do_login is used
        self.logged_in = False

        # We use the FMG class for any FMG API (and caching?) operations
        self.fmg = FMG()

        # We use the FMGFS class for creating a kind of FMG file system
        self.fmg_fs = FMGFS("root")

        # The current working directory in the FMG file system
        self.working_directory = self.fmg_fs

        # Debug file
        self.debug_file = "fmgshell.debug"
        self.debug_fh = open(self.debug_file, "a")

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
                self.poutput(fmgshell_print_get_system_status(response))
        else:
            self.poutput("You need to login first.")

    cmd2.categorize(do_get, CMD2_CATEGORY)

    # Print working directory
    def do_pwd(self, args):
        """Print working directory."""
        self.poutput(self.working_directory.get_full_path())

    cmd2.categorize(do_pwd, CMD2_CATEGORY)

    # Change working directory
    def do_cd(self, args):
        """Change working directory."""
        if self.logged_in:
            dest_dir = str(args)
            if len(dest_dir) == 0 or dest_dir == "/":

                self.working_directory = self.fmg_fs
            else:
                try:
                    if dest_dir[0] == "/":
                        node = self.fmg_fs.get_node_by_path(dest_dir)
                    else:
                        node = self.working_directory.get_node_by_path(dest_dir)
                except FMGFS_WrongPath:
                    print("Wrong path.")
                else:
                    self.working_directory = node
        else:
            self.poutput("You need to login first.")

    cmd2.categorize(do_cd, CMD2_CATEGORY)

    def complete_cd(self, text, line, begidx, endidx):

        if self.logged_in:
            pass
        else:
            return []

        # We need to work with the absolute path
        full_path_text = None

        try:
            if text[0] == "/":
                full_path_text = text
        except IndexError:
            pass

        if not full_path_text:
            path_prefix = self.working_directory.get_full_path()

            # if wd is "/"
            if path_prefix == "/":
                full_path_text = f"{path_prefix}{text}"
            else:
                full_path_text = f"{path_prefix}/{text}"

        matches = fmgshell_get_matching_paths(self, full_path_text)

        results = cmd2.utils.basic_complete(
            full_path_text, line, begidx, endidx, matches
        )

        # Prevent to append a space when completion is done - Inherited from
        # cmd2.Cmd
        if len(results) == 1:
            self.allow_appended_space = False

        if True:
            print(file=self.debug_fh, flush=True)
            print(f"Result: {results}", file=self.debug_fh, flush=True)
            print(f"Text: {text}", file=self.debug_fh, flush=True)
            print(f"Full path text: {text}", file=self.debug_fh, flush=True)
            print(f"Type(Text)): {type(text)}", file=self.debug_fh, flush=True)
            print(f"Line: {line}", file=self.debug_fh, flush=True)
            print(f"Begidx: {begidx}", file=self.debug_fh, flush=True)
            print(f"Endidx: {endidx}\n", file=self.debug_fh, flush=True)
            print(file=self.debug_fh, flush=True)

        return results