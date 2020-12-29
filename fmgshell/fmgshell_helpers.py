# coding=utf-8
"""Helpers for fmgshell operations."""

import json
from fmgfs import FMGFS


def fmgshell_print_get_system_status(response):
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


def fmgshell_get_matching_paths(fmgshell, text):
    """
    Return list of FMG FS path that match with text.

    Note: text can only be a absolute path name

    Args:
        fmgshell (FMGSHELL): a FMGSHELL instance
        text (str): the text to be matched with

    Returns:
        (list): list of matching paths
    """
    matching_paths = []

    if len(text) == 0:
        matching_paths = fmgshell.working_directory.get_children_by_name()
    elif text == "/":
        matching_paths = fmgshell.fmg_fs.get_children_by_name()
        n_matching_paths = len(matching_paths)
        for i in range(n_matching_paths):
            name = "/" + matching_paths[i]
            matching_paths[i] = name
    else:
        # From where to start in the FMG FS?
        # Check whether text is an absolute path
        if text[0] == "/":
            node = fmgshell.fmg_fs
        else:
            node = FMGFS("root")
            node.add_child(fmgshell.working_directory)

        # we navigate as far as we can

    print(matching_paths)

    return matching_paths
