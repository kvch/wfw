import requests
import json
from wfw.wfexceptions import LoginFailedException
from wfw.tree import Tree

class WorkFlowy(object):

    wfurl = 'https://workflowy.com/'

    def __init__(self):
        self.session_id = None
        self.tree = Tree()

    def __log_in(self, email, password):
        info = {'username' : email, 'password': password, 'next' : ''}
        req = requests.post(self.wfurl + 'accounts/login/', data=info)

        if not len(req.history) == 1:
            raise LoginFailedException("Login was not successful")

        cookies = requests.utils.dict_from_cookiejar(req.history[0].cookies)
        self.session_id = cookies['sessionid']

    def __log_out(self):
        cookie = {'sessionid' : self.session_id}
        req = requests.get(self.wfurl + 'offline_logout', cookies=cookie)

    def __fetch_list(self):
        cookie = {'sessionid' : self.session_id}
        req = requests.post(self.wfurl + 'get_initialization_data?client_version=14',
                            cookies=cookie)

        tree = req.json()
        tree_data = open('tree', 'w')
        json.dump(tree, tree_data)
        tree_data.close()

    def __build_tree_from_file(self):
        raw_data = open('tree', 'r')
        self.tree.build(raw_data.read())


    def get_list(self, email, password):
        try:
            self.__log_in(email, password)
        except LoginFailedException:
            raise
        else:
            self.__fetch_list()
            self.__log_out()

    def update(self):
        req = requests.post(self.wfurl + 'push_and_pull')

    def print_list(self, depth, root=None):
        self.__build_tree_from_file()
        if root is None:
            self.tree.print_tree(self.tree.root, depth)
        else:
            self.tree.print_subtree(root, depth)

    def export_list(self, file_name):
        self.__build_tree_from_file()
        self.tree.export_tree(file_name)

    def search_tags(self, tag):
        self.__build_tree_from_file()
        self.tree.print_nodes_with_tag(tag)
