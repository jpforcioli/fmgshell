# coding=utf-8
"""Helpers for fmgshell operations."""

import os.path

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


def fmgshell_get_matching_paths(fmgshell, full_path_text):
    """
    Return list of FMG FS path that match with text.

    Args:
        fmgshell (FMGSHELL): a FMGSHELL instance
        full_path_text (str): the text to be matched with; should always be an
        absolute path

    Returns:
        (list): list of matching paths
    """
    # Get the node matching the best the full_path_text
    node = fmgshell.fmg_fs.get_node_by_path(full_path_text, best_match=True)

    # Get the content for selected node
    matches = node.get_children_by_name()

    # We replace each match element with an absolute path
    path_prefix = node.get_full_path()
    if path_prefix == "/":
        matches = [f"{path_prefix}{element}/" for element in matches]
    else:
        matches = [f"{path_prefix}/{element}/" for element in matches]

    # Completion should only display last part of the path
    # cmd2.Cmd.display_matches is containing what completion offers as choices
    # to the user, but completion still work on "matches".
    fmgshell.display_matches = [
        os.path.basename(element.rstrip("/")) for element in matches
    ]

    if True:
        print(file=fmgshell.debug_fh, flush=True)
        print(
            f"fmgshell_get_matching_paths: node: {node}",
            file=fmgshell.debug_fh,
            flush=True,
        )
        print(
            f"fmgshell_get_matching_paths: matches: {matches}",
            file=fmgshell.debug_fh,
            flush=True,
        )
        print(
            f"fmgshell_get_matching_paths: display_matches: {fmgshell.display_matches}",
            file=fmgshell.debug_fh,
            flush=True,
        )
        print(
            f'fmgshell_get_matching_paths: full_path_text: "{full_path_text}"',
            file=fmgshell.debug_fh,
            flush=True,
        )
        print(file=fmgshell.debug_fh, flush=True)

    return matches

    # Still blocked, I really need to review how path_complete() works...
