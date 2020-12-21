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
        self.http_session = requests.Session()
        self.http_session.verify = False
        self.json_rpc = {"id": 0, "session": None}
        self._debug = "off"

    def debug(self, flag="show"):
        """
        Turn on/off debug mode.

        Args:
            flag (str)
        """
        if flag in ["on", "off"]:
            self._debug = flag
        elif flag == "show":
            return self._debug
        else:
            raise WrongDebugFlag

    def print_debug(self, response):
        """
        Print FortiManager JSON RPC API REQUEST/RESPONSE.

        Args:
            response (dict): the requests.Session.Response object
        """
        if self._debug == "on":
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
        self.json_rpc["id"] = self.json_rpc["id"] + 1

        return self.json_rpc["id"]

    def post_json_rpc(self, payload):
        """
        Complete and send the JSON RPC payload.

        Args:
            payload (dic): The JSON RPC payload

        Returns:
            (dict): The JSON RPC output
        """
        payload["session"] = self.json_rpc["session"]
        payload["id"] = self.consume_id()

        response = self.http_session.post(self.base_url, json=payload)
        response.raise_for_status()

        self.print_debug(response)

        return response.json()

    def login(self, ip, username, password, port=443, proto="https"):
        """
        Login to FortiManager.

        Arguments
        ---------
        ip: str
            FortiManager IP address or FQDN
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
        }

        response = self.post_json_rpc(payload)

        try:
            self.json_rpc["session"] = response["session"]
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
        }

        response = self.post_json_rpc(payload)

    def get(self, url):
        """
        Implement the FMG JSON RPC API "get" method

        Args:
            url (str): The FMG JSON RPC API url
        """

        payload = {
            "method": "get",
            "params": [
                {
                    "url": url,
                },
            ],
        }

        return self.post_json_rpc(payload)


if __name__ == "__main__":
    fmg = FMGJSONRPCAPI()
    fmg.debug("on")
    fmg.login("secops-labs-004.gcp.fortipoc.net", "devops", "fortinet", port=10407)
    fmg.logout()