# coding: utf-8

"""A class to represent a FortiManager."""


class FMG:
    """A FortiManager class."""

    def __init__(self):
        self.system_status = None
        pass

    def get_system_status(self, fmg_api, force_refresh=False):
        """
        Get the FortiManager system status.

        Args:
            fmg_api (class FMGJSONRPCAPI): an instance of the class FMGJSONRPCAPI
            force_refresh (bool, optional): force a request. Defaults to False.

        Returns:
            [dict]: the list of items composing the "get system status"
        """
        if self.system_status == None or force_refresh:
            url = "/cli/global/system/status"
            response = fmg_api.get(url)
            self.system_status = response["result"][0]["data"]

        return self.system_status
