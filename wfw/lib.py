from ConfigParser import RawConfigParser
from os.path import expanduser, isfile
import json

from wfw.api import log_in, log_out, get_list_from_server, post_local_change
from wfw.tree import Tree
from wfw.wfexceptions import LocalChangePostingError, NodeNotFoundError


TREE_DATA = expanduser('~/.wfwtree')
USER_DATA = expanduser('~/.wfwrc')


def get_tree_from_file():
    tree = None
    with open(TREE_DATA, 'r') as tree_data:
        tree = Tree(json.load(tree_data))
    return tree


def get_user_data():
    if isfile(USER_DATA):
        configparser = RawConfigParser()
        user_data = {}
        with open(USER_DATA) as config:
            configparser.readfp(config)
        user_data['email'] = configparser.get('user', 'email')
        user_data['password'] = configparser.get('user', 'password')
        user_data['aux'] = configparser.get('tree', 'shared')
        return user_data


def fetch_list():
    user = get_user_data()
    try:
        session_id = log_in(user['email'], user['password'])
    except Exception:
        raise
    else:
        get_list_from_server(session_id)
        log_out(session_id)


def print_list(depth, selected_root=None):
    tree = get_tree_from_file()
    try:
        if selected_root is None:
            tree.print_by_node(depth)
        else:
            tree.print_by_name(selected_root, depth)
    except NodeNotFoundError:
        raise


def export_list(file_name):
    tree = get_tree_from_file()
    tree.export(file_name)


def search_nodes(pattern):
    tree = get_tree_from_file()
    result = tree.find_nodes(tree.root, pattern)
    tree.print_node_list(result)


def search_tags(tag):
    tree = get_tree_from_file()
    result = tree.find_tag(tree.root, tag)
    tree.print_node_list(result)


def add_item(parent_item, new_item):
    tree = get_tree_from_file()
    parent_node = tree.get_node(self.root, parent_item)
    user = get_user_data()
    try:
        session_id = log_in(user['email'], user['password'])
        post_local_change(session_id, 'add', parent_node['id'], new_item)
    except LocalChangePostingError:
        log_out(session_id)
        raise
    except Exception:
        raise
    else:
        get_list_from_server(session_id)
        log_out(session_id)


def remove_item(parent_item, deleted_item):
    tree = get_tree_from_file()
    parent_node = tree.get_node(tree.root, parent_item)
    deleted_node = tree.get_node(tree.root, deleted_item)
    user = get_user_data()
    try:
        session_id = log_in(user['email'], user['password'])
        post_local_change(session_id, 'rm', parent_node['id'], deleted_item, deleted_node['id'])
    except LocalChangePostingError:
        log_out(session_id)
        raise
    except Exception:
        raise
    else:
        get_list_from_server(session_id)
        log_out(session_id)


def calc_item_stats(item):
    tree = get_tree_from_file()
    node = tree.get_node(tree.root, item)
    number_children, done = tree.get_node_info(node)
    if node['done']:
        done = done - 1
    if number_children > 0:
        progress = round(done / float(number_children) * 100, 2)
    else:
        progress = 0
    tree.print_node_list([node])
    tree.print_stats(number_children, done, progress)

def show_agenda(item):
    tree = get_tree_from_file()
    node = tree.get_node(tree.root, item)
    if node:
        events = tree.get_agenda(node)
        tree.print_agenda(events)
