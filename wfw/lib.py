from os.path import expanduser, isfile
from ConfigParser import RawConfigParser
from wfw.wfexceptions import LoginFailedException, NodeNotFoundError, LocalChangePostingError
from wfw.api import log_in, log_out, get_list_from_server, post_local_change
from wfw.tree import build, print_by_node, print_by_name, print_node_list, export_tree, find_nodes, find_tag


TREE_DATA = expanduser('~/.wfwtree')
USER_DATA = expanduser('~/.wfwrc')
ROOT = {'id' : 0, 'text' : 'My list', 'children' : [], 'done' : False}


def build_tree_from_file():
    with open(TREE_DATA, 'r') as tree_data:
        build(tree_data, ROOT)


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
    result = find_nodes(ROOT, regex)
    print_node_list(result)


def search_tags(tag):
    build_tree_from_file()
    result = find_tag(ROOT, tag)
    print_node_list(result) 


def add_item(parent_item, new_item):
    build_tree_from_file()
    parent_node = find_node(ROOT, parent_item)
    user = get_user_data()
    session_id = log_in(user['email'], user['password'])
    try:
        post_local_change(session_id, 'add', parent_node['id'], new_item)
    except LocalChangePostingError:
        log_out(session_id)
        raise
    else:
        get_list_from_server(session_id)
        log_out(session_id)


def remove_item(parent_item, deleted_item):
    build_tree_from_file()
    parent_node = find_node(ROOT, parent_item)
    deleted_node = find_node(ROOT, deleted_item)
    user = get_user_data()
    session_id = log_in(user['email'], user['password'])
    try:
        post_local_change(session_id, 'rm', parent_node['id'], deleted_item, deleted_node['id'])
    except LocalChangePostingError:
        log_out(session_id)
        raise
    else:
        get_list_from_server(session_id)
        log_out(session_id)
