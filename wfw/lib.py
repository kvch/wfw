from ConfigParser import RawConfigParser
from os.path import expanduser, isfile

from wfw.api import log_in, log_out, get_list_from_server, post_local_change
from wfw.tree import (build,
                      export_tree,
                      find_nodes,
                      find_tag,
                      get_agenda,
                      get_node,
                      get_node_info,
                      print_agenda,
                      print_by_name,
                      print_by_node,
                      print_node_list,
                      print_stats)
from wfw.wfexceptions import LocalChangePostingError, NodeNotFoundError


TREE_DATA = expanduser('~/.wfwtree')
USER_DATA = expanduser('~/.wfwrc')
ROOT = {'id' : 0, 'text' : 'My list', 'children' : [], 'done' : False}


def build_tree_from_file():
    with open(TREE_DATA, 'r') as tree_data:
        build(tree_data, ROOT)


def get_user_data():
    if isfile(USER_DATA):
        configparser = RawConfigParser()
        user_data = {}
        with open(USER_DATA) as config:
            configparser.readfp(config)
        user_data['email'] = configparser.get('user', 'email')
        user_data['password'] = configparser.get('user', 'password')
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
    build_tree_from_file()
    try:
        if selected_root is None:
            print_by_node(ROOT, depth)
        else:
            print_by_name(selected_root, depth, ROOT)
    except NodeNotFoundError:
        raise


def export_list(file_name):
    build_tree_from_file()
    export_tree(file_name, ROOT)


def search_nodes(pattern):
    build_tree_from_file()
    result = find_nodes(ROOT, pattern)
    print_node_list(result)


def search_tags(tag):
    build_tree_from_file()
    result = find_tag(ROOT, tag)
    print_node_list(result)


def add_item(parent_item, new_item):
    build_tree_from_file()
    parent_node = get_node(ROOT, parent_item)
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
    build_tree_from_file()
    parent_node = get_node(ROOT, parent_item)
    deleted_node = get_node(ROOT, deleted_item)
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
    build_tree_from_file()
    node = get_node(ROOT, item)
    number_children, done = get_node_info(node)
    if node['done']:
        done = done - 1
    if number_children > 0:
        progress = round(done / float(number_children) * 100, 2)
    else:
        progress = 0
    print_node_list([node])
    print_stats(number_children, done, progress)

def show_agenda(item):
    build_tree_from_file()
    node = get_node(ROOT, item)
    if node:
        events = get_agenda(node)
        print_agenda(events)
