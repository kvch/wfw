import json
from os.path import expanduser
from wfw.wfexceptions import LoginFailedException
from wfw.api import log_in, log_out, get_list_from_server
from wfw.tree import Tree


TREE_DATA = expanduser('~/.wfwtree')


def build_tree_from_file():
    tree = Tree()
    with open(TREE_DATA, 'r') as tree_data:
        tree.build(tree_data)
        return tree


def fetch_list(email, password):
    try:
        session_id = log_in(email, password)
    except LoginFailedException:
        raise
    else:
        get_list_from_server(session_id)
        log_out(session_id)


def print_list(depth, root=None):
    tree = build_tree_from_file()
    if root is None:
        tree.print_subtree(tree.root, depth)
    else:
        tree.print_tree(root, depth)


def export_list(file_name):
    tree = build_tree_from_file()
    tree.export_tree(file_name)


def search_tags(tag):
    tree = build_tree_from_file()
    tree.print_nodes_with_tag(tag)
