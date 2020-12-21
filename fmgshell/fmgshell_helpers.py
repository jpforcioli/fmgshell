# coding=utf-8
"""Helpers for fmgshell operations."""


def fmg_print_get_system_status(response):
    """
    Print the FortiManager "get system status" output.

    Args:
        response (dict): The JSCON RPC output containing the "get system
        status".

    Returns:
        contant (str): the formatted output
    """
    # Retrieve the longest key
    l_key = max(response.keys(), key=lambda s: len(str(s)))
    key_len = len(l_key) + 1

    # Retrieve the longest value
    l_value = max(response.values(), key=lambda s: len(str(s)))
    value_len = len(l_value)

    content = ""

    for key in response:
        content = content + f"{key:<{key_len}}: {response[key]:<{value_len}}" + "\n"

    return content
