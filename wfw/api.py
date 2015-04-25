from os.path import expanduser
import json
import random
import requests
import string
import uuid

from wfw.wfexceptions import LoginFailedException, LocalChangePostingError


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


def prepare_new_item(parent_id, name, client_timestamp):
    new_id = str(uuid.uuid4())

    new_node_place = {'projectid' : new_id,
                      'parentid' : parent_id,
                      'priority' : 999}

    new_node_data = {'projectid' : new_id,
                     'name' : name}

    operation = [{'type' : 'create',
                  'data' : new_node_place,
                  'client_timestamp' : client_timestamp,
                  'undo_data' : {}},
                 {'type' : 'edit',
                  'data' : new_node_data,
                  'client_timestamp' : client_timestamp,
                  'undo_data': {'previous_last_modified' : client_timestamp,
                                'previous_name' : ''}}]

    return operation


def prepare_deleted_item(parent_id, deleted_id, client_timestamp):
    deleted_node = {'projectid' : deleted_id}

    operation = [{'type' : 'delete',
                  'data' : deleted_node,
                  'client_timestamp' : client_timestamp,
                  'undo_data': {'previous_last_modified' : client_timestamp,
                                'parentid' : parent_id,
                                'priority' : 0}}]

    return operation


def post_local_change(session_id, operation, parent_id, name, deleted_id=None):
    with open(TREE_DATA, 'r') as tree_data:
        config = json.load(tree_data)

    client_timestamp = config['projectTreeData']['mainProjectTreeInfo']['dateJoinedTimestampInSeconds'] / 60
    most_recent_op = config['projectTreeData']['mainProjectTreeInfo']['initialMostRecentOperationTransactionId']
    client_id = config['projectTreeData']['clientId']

    push_poll_id = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(8))

    operation_data = []
    if operation == 'add':
        operation_data = prepare_new_item(parent_id, name, client_timestamp)
    elif operation == 'rm':
        operation_data = prepare_deleted_item(parent_id, deleted_id, client_timestamp)

    push_poll_data = [{'most_recent_operation_transaction_id' : most_recent_op,
                       'operations' : operation_data}]

    push_poll_data = json.dumps(push_poll_data)

    payload = {'client_id' : client_id,
               'client_version' : 14,
               'push_poll_id' : push_poll_id,
               'push_poll_data' : push_poll_data}

    cookie = {'sessionid' : session_id}

    request = requests.post(WFURL + 'push_and_poll', data=payload, cookies=cookie)

    if request.status_code != 200:
        raise LocalChangePostingError
