import requests
import json
import uuid
import random
import string
from os.path import expanduser
from wfw.wfexceptions import LoginFailedException


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


def post_new_item(parent_id, name, session_id):
    new_id = str(uuid.uuid4())

    with open(TREE_DATA, 'r') as tree_data:
        config = json.load(tree_data)

    client_timestamp = config['projectTreeData']['mainProjectTreeInfo']['dateJoinedTimestampInSeconds'] / 60
    most_recent_op = config['projectTreeData']['mainProjectTreeInfo']['initialMostRecentOperationTransactionId']
    client_id = config['projectTreeData']['clientId']

    push_poll_id = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(8))

    new_node_place = {'projectid' : new_id,
                      'parentid' : parent_id,
                      'priority' : 999}

    new_node_data = {'projectid' : new_id,
                     'name' : name}

    push_poll_data = [{'most_recent_operation_transaction_id' : most_recent_op,
                       'operations' : [{'type' : 'create',
                                        'data' : new_node_place,
                                        'client_timestamp' : client_timestamp,
                                        'undo_data' : {}},
                                       {'type' : 'edit',
                                        'data' : new_node_data,
                                        'client_timestamp' : client_timestamp,
                                        'undo_data': {'previous_last_modified' : client_timestamp,
                                                      'previous_name' : ''}}]}]
    push_poll_data = json.dumps(push_poll_data)

    payload = {'client_id' : client_id,
               'client_version' : 14,
               'push_poll_id' : push_poll_id,
               'push_poll_data' : push_poll_data}

    cookie = {'sessionid' : session_id}

    request = requests.post(WFURL + 'push_and_poll', data=payload, cookies=cookie)

    if request.status_code == 200:
        return new_id

    return None
