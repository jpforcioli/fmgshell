# coding= utf-8
"""FortiManager JSON RPC API."""

import json
import requests

# To disable SSL warning
from urllib3.exceptions import InsecureRequestWarning

# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

from exceptions import *


class FMGJSONRPCAPI:
    """FMG JSON RPC API Class."""

    def __init__(self):
        self.session = requests.Session()
        self.session.verify = False
        self.id = 0
        self.session_id = None
        self.do_debug = "off"

    def debug(self, flag="show"):
        """
        Turn on/off debug mode.

        Args:
            flag (str)
        """
        if flag in ["on", "off"]:
            self.do_debug = flag
        elif flag == "show":
            return self.do_debug
        else:
            raise WrongDebugFlag

    def print_debug(self, response):
        """
        Print FortiManager JSON RPC API REQUEST/RESPONSE.

        Args:
            response (dict): the requests.Session.Response object
        """
        if self.do_debug == "on":
            http_method = response.request.method
            http_req_body = json.loads(response.request.body)
            http_res_body = response.json()

            print("REQUEST:")
            print()
            print(f"{json.dumps(http_req_body, indent=4)}")
            print()

            print("RESPONSE:")
            print()
            print(f"{json.dumps(http_res_body, indent=4)}")
            print()

    def consume_id(self):
        """
        Get next available JSON RPC ID.

        Return
        ------
        int
        """
        self.id = self.id + 1

        return self.id

    def login(self, ip, username, password, port=443, proto="https"):
        """
        Login to FortiManager.

        Arguments
        ---------
        ip: str
            FortiManager IP address
        username: str
            FortiManager username
        password: str
            FortiManager password
        port: int
            FortiManager port (default is 443)
        proto: string
            "http" or "https" (default is "https")
        """

        self.base_url = f"{proto}://{ip}:{port}/jsonrpc"
        jsonrpc_url = "/sys/login/user"
        payload = {
            "method": "exec",
            "params": [
                {
                    "data": {
                        "user": username,
                        "passwd": password,
                    },
                    "url": jsonrpc_url,
                },
            ],
            "session": self.session_id,
            "id": self.consume_id(),
        }

        response = self.session.post(self.base_url, json=payload)
        response.raise_for_status()

        self.print_debug(response)

        try:
            self.session_id = response.json()["session"]
        except KeyError as error:
            print("ERROR: No session ID was returned.")
            print("ERROR: Please double check your login/password.")

    def logout(self):
        """
        Logout from FortiManager.
        """

        jsonrpc_url = "/sys/logout"
        payload = {
            "method": "exec",
            "params": [
                {
                    "url": "/sys/logout",
                },
            ],
            "session": self.session_id,
            "id": self.consume_id(),
        }

        response = self.session.post(self.base_url, json=payload)
        response.raise_for_status()

        self.print_debug(response)


if __name__ == "__main__":
    fmg = FMGJSONRPCAPI()
    fmg.debug("on")
    fmg.login("secops-labs-004.gcp.fortipoc.net", "devops", "fortinet", port=10407)
    fmg.logout()