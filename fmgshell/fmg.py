# coding: utf-8

"""A class to represent a FortiManager."""

from fmgjsonrpcapi import FMGJSONRPCAPI


class FMG:
    """A FortiManager class."""

    def __init__(self):
        self.api = FMGJSONRPCAPI()
        self.system_status = None
        self.adoms_cache = {
            "adom_list": [],
            "checksum": None,
        }

    def login(self, ip, username, password, port):
        """Login to FortiManager.

        Args:
            ip (str): FortiManager IP address or FQDN
            username (str): FortiManager username
            password (str): FortiManager password
            port (int): FortiManager port (default is 443)
        """
        self.api.login(ip, username, password, port)

    def logout(self):
        """Logout from FortiManager."""

        self.api.logout()

    def get(self, url, attributes=None):
        """Get a table or an object definition.

        Args:
            url (str): The path to the table or the object.
            attributes (dict): The list of extra attributes like "option",
                               "fields", "filter", etc.

        Returns:
            (dict) The table or object definition.
        """

        return self.api.get(url, attributes)

    def debug(self, flag="show"):
        return self.api.debug(flag)

    def get_system_status(self, force_refresh=False):
        """
        Get the FortiManager system status.

        Args:
            force_refresh (bool, optional): force a request. Defaults to False.

        Returns:
            [dict]: the list of items composing the "get system status"
        """
        if self.system_status == None or force_refresh:
            url = "/cli/global/system/status"
            response = self.api.get(url)
            self.system_status = response["result"][0]["data"]

        return self.system_status

    def get_checksum(self, url):
        """
        Retrieve the checksum for the specified table or object.

        Args:
            url (str): The FortiManager table of object.

        Returns:
            (str): The checksum
        """
        attributes = {"option": "devinfo"}
        response = self.get(url, attributes)
        return response["result"][0]["data"]["uuid"]

    def get_adoms(self):
        """
        Get the ADOM list.

        Returns:
            (list): the ADOM list
        """
        url = "/dvmdb/adom"
        # First retrieve the checksum
        checksum = self.get_checksum(url)

        if checksum != self.adoms_cache["checksum"]:
            attributes = {
                "filter": [
                    "restricted_prds",
                    "==",
                    "fos",
                ],
                "fields": ["name"],
                "loadsub": 0,
            }
            response = self.get(url, attributes)

            adom_list = []
            for adom in response["result"][0]["data"]:
                name = adom["name"]
                if name == "rootp":
                    name = "global"
                adom_list.append(name)

            # We update the cached checksum and adom_list
            self.adoms_cache["checksum"] = checksum
            self.adoms_cache["adom_list"] = adom_list

        return self.adoms_cache["adom_list"]


if __name__ == "__main__":
    ip = "secops-labs-004.gcp.fortipoc.net"
    # ip = "10.210.35.200"
    port = 10407
    # port = 443
    username = "admin"
    password = "fortinet"

    fmg = FMG()
    fmg.login(ip, username, password, port)
    fmg.debug("off")
    fmg.get_adoms()
    fmg.debug("off")
    fmg.logout()