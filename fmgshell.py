# coding= utf-8
"""fmgshell: a shell to operate FortiManager."""

import argparse
import getpass

import cmd2

from fmgjsonrpcapi import FMGJSONRPCAPI


class FMGShell(cmd2.Cmd):
    """Sub-class of the cmd2.Cmd."""

    def __init__(self):
        self.prompt = "fmgshell> "
        self.continuation_prompt = "> "
        self.fmg = FMGJSONRPCAPI()
        super().__init__()

    # Login to FMG
    login_parser = argparse.ArgumentParser()
    login_parser.add_argument(
        "-i", "--ip", required=True, help="FortiManager IP address"
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
        fmg_ip = args.ip
        fmg_username = args.username
        fmg_password = args.password
        fmg_port = args.port
        if fmg_password == None:
            fmg_password = getpass.getpass()
        if fmg_port == None:
            fmg_port = 443

        self.fmg.login(fmg_ip, fmg_username, fmg_password, fmg_port)

    # Logout from FMG
    def do_logout(self, args):
        """Logout from FortiManager."""
        self.fmg.logout()

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


if __name__ == "__main__":
    shell = FMGShell()

    shell.cmdloop()
