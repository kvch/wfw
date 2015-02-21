from os.path import expanduser, isfile
from ConfigParser import RawConfigParser
from wfw.wfexceptions import LoginFailedException, NodeNotFoundError
from wfw.api import log_in, log_out, get_list_from_server, post_new_item
from wfw.tree import Tree


TREE_DATA = expanduser('~/.wfwtree')
USER_DATA = expanduser('~/.wfwrc')


def build_tree_from_file():
    tree = Tree()
    with open(TREE_DATA, 'r') as tree_data:
        tree.build(tree_data)
    return tree


def get_user_data():
    configparser = RawConfigParser()
    user_data = {}
    with open(USER_DATA) as config:
        configparser.readfp(config)
    user_data['email'] = configparser.get('user', 'email')
    user_data['password'] = configparser.get('user', 'password')
    return user_data


def fetch_list(email, password):
    if isfile(USER_DATA):
        user_data = get_user_data()
        email, password = user_data['email'], user_data['password']
    try:
        session_id = log_in(email, password)
    except LoginFailedException:
        raise
    else:
        get_list_from_server(session_id)
        log_out(session_id)


def print_list(depth, root=None):
    tree = build_tree_from_file()
    try:
        if root is None:
            tree.print_by_node(tree.root, depth)
        else:
            tree.print_by_name(root, depth)
    except NodeNotFoundError:
        raise


def export_list(file_name):
    tree = build_tree_from_file()
    tree.export_tree(file_name)


def search_tags(tag):
    tree = build_tree_from_file()
    tree.print_nodes_with_tag(tag)

def add_item(parent_item, new_item):
    tree = build_tree_from_file()
    parent_node = tree.find_node(tree.root, parent_item)
    user = get_user_data()
    session_id = log_in(user['email'], user['password'])
    post_new_item(parent_node.node_id, new_item, session_id)
    log_out(session_id)
