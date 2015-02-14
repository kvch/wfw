import requests
import json
from os.path import expanduser
from wfw.wfexceptions import LoginFailedException
from wfw.tree import Tree


WFURL = 'https://workflowy.com/'
TREE_DATA = expanduser('~/.wfwtree')


def log_in(email, password):
    info = {'username' : email, 'password': password, 'next' : ''}
    request = requests.post(WFURL + 'accounts/login/', data=info)

    if not len(request.history) == 1:
        raise LoginFailedException("Login was not successful")

    cookies = requests.utils.dict_from_cookiejar(request.history[0].cookies)
    return cookies['sessionid']


def log_out(session_id):
    cookie = {'sessionid' : session_id}
    requests.get(WFURL + 'offline_logout', cookies=cookie)


def get_list_from_server(session_id):
    cookie = {'sessionid' : session_id}
    request = requests.post(WFURL + 'get_initialization_data?client_version=14',
                            cookies=cookie)

    tree = request.json()
    with open(TREE_DATA, 'w') as tree_data:
        json.dump(tree, tree_data)


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
