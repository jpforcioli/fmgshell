# coding: utf-8

"""A class to represent a FortiManager."""

from fmgjsonrpcapi import FMGJSONRPCAPI


class FMG:
    """A FortiManager class."""

    def __init__(self):
        self.api = FMGJSONRPCAPI()
        self.system_status = None
        pass

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
