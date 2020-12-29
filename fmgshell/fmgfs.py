# coding: utf-8
"""Class for FortiManager File System."""

import json

FMG_SUPPORTED_PATH = "fmg_supported_path"


class FMGFS_EXCEPTION(Exception):
    def __init__(self):
        pass


class FMGFS_WrongPath(FMGFS_EXCEPTION):
    def __init__(self):
        pass


class Node:
    """Class to represent a FMG FS element."""

    def __init__(self, name):
        """
        Class to represent a FMG FS element.

        Args:
            name ([type]): [description]
        """
        self.name = name
        self.parent = None
        self.children = []

    def add_child(self, child):
        """
        Add a child node.

        Args:
            child (Node): a child node
        """
        child.parent = self
        self.children.append(child)

    def set_parent(self, parent):
        """
        Add a parent node.

        Args:
            parent (Node): the parent node
        """
        self.parent = parent
        parent.children.append(self)

    def nprint(self, n=0):
        """
        nprint for Node Print.

        Print a node along with its children in a hierarchical form.

        Args:
            n (int, optional): Indentation. Defaults to 0.
        """
        pad = " " * n
        print(f"{pad}{self.name}")
        for child in self.children:
            child.nprint(n + 2)

    def is_child_by_name(self, name):
        """
        Check whether there is child with this name.

        Args:
            name (str): the name to be checked

        Returns:
            The child index or None.
        """
        result = None
        idx = 0
        for child in self.children:
            if child.name == name:
                result = idx
                break
            idx = idx + 1

        return result

    def get_children_by_name(self):
        """
        Get the list of children's names.

        Returns:
            (list): list of children's names
        """
        names_list = []
        for child in self.children:
            names_list.append(child.name)

        return names_list

    def get_node_by_path(self, path):
        path = path.lstrip("/")
        elements = path.split("/")

        node = self
        for element in elements:
            idx = node.is_child_by_name(element)
            if idx == None:
                raise FMGFS_WrongPath
            node = node.children[idx]

        return node

    def get_full_path(self):
        """
        Get the full path.

        Returns:
            (str): the full path name.
        """
        node = self
        full_path = [node.name]
        while node.parent != None:
            node = node.parent
            full_path.append(node.name)

        full_path.append("")
        full_path.reverse()
        if len(full_path) == 2:
            return "/"
        else:
            del full_path[1]

        return "/".join(full_path)

    def load(self, file=FMG_SUPPORTED_PATH):
        """
        Create the FMG FS from a file.

        File is a list of PATHs.

        Args:
            file (str, optional): The file containing the supported path.
            Defaults to FMG_SUPPORTED_PATH.
        """
        with open(file, "r") as f:
            for line in f:
                node = self
                line = line.lstrip("/")
                elements = line.split("/")
                for element in elements:
                    # Check whether element exists in list of children
                    idx = node.is_child_by_name(element)
                    if idx == None:
                        # Does not exist; we create it
                        new_child = Node(element)
                        node.add_child(new_child)
                        node = new_child
                    else:
                        node = node.children[idx]


class FMGFS(Node):
    """Class for FortiManager File System."""

    def __init__(self, name):
        super().__init__(name)
        self.load()


if __name__ == "__main__":
    root = FMGFS("root")
    root.load()
    root.nprint()