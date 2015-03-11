import json
from wfw.wfexceptions import NodeNotFoundError, InvalidTagFormatException

class Tree(object):

    def __init__(self):
        self.root = Node(0, 'My list', None)


    def __eq__(self, other):
        self.__eq_by_node(self.root, other.root)
        return True


    def __neq__(self, other):
        return not self.__eq__(other)


    def __eq_by_node(self, this_node, other_node):
        if this_node != other_node:
            return False

        for i in range(len(this_node.children)):
            self.__eq_by_node(this_node.children[i], other_node.children[i])


    def __add_node(self, node, parent):
        new_node = Node(node['id'], node['nm'].encode('utf-8'), parent)
        parent.add_child(new_node)

        if 'ch' in node.keys():
            for child in node['ch']:
                self.__add_node(child, new_node)


    def find_node(self, node, name_to_find):
        if node.name == name_to_find.encode('utf-8'):
            return node

        for child in node.children:
            result = self.find_node(child, name_to_find)
            if result:
                return result


    def __find_tag(self, node, tag, result=[]):
        if tag[0] == '#' or tag[0] == '@':
            for child in node.children:
                if tag.encode('utf-8') in child.name:
                    result.append(child)
                self.__find_tag(child, tag, result)

            return result


    def __write_to_file(self, destination, start, depth=0):
        destination.write(start.exportable_format(depth))
        for child in start.children:
            self.__write_to_file(destination, child, depth+1)


    def build(self, input_file):
        raw_tree = json.load(input_file)
        children_of_root = raw_tree['projectTreeData']['mainProjectTreeInfo']['rootProjectChildren']

        for child in children_of_root:
            self.__add_node(child, self.root)


    def print_by_node(self, start, depth, current_depth=0):
        print(start.printable_format(current_depth))

        if depth > current_depth:
            current_depth += 1
            for child in start.children:
                self.print_by_node(child, depth, current_depth)


    def print_by_name(self, name, depth):
        root = self.find_node(self.root, name)

        if not root is None:
            self.print_by_node(root, depth)
        else:
            raise NodeNotFoundError


    def export_tree(self, file_name):
        with open(file_name, 'w') as destination:
            self.__write_to_file(destination, self.root)


    def print_nodes_with_tag(self, tag):
        result = self.__find_tag(self.root, tag)
        if result is None:
            raise InvalidTagFormatException("Tag has to start with # or @")

        for node in result:
            print(node.printable_format())


class Node(object):

    def __init__(self, node_id, name, parent):
        self.node_id = node_id
        self.name = name
        self.parent = parent
        self.children = []

    def __eq__(self, other):
        if self.name != other.name:
            return False
        if self.node_id != other.node_id:
            return False
        if self.parent != other.parent:
            return False
        if len(self.children) != len(other.children):
            return False
        for i in range(len(self.children)):
            if self.children[i] != other.children[i]:
                return False

        return True


    def __neq__(self, other):
        return not self.__eq__(other)


    def add_child(self, child):
        self.children.append(child)


    def exportable_format(self, depth):
        return "{fill}{name}\n".format(fill='\t' * depth, name=self.name)


    def printable_format(self, depth=0):
        return "{fill}* {name}".format(fill='    ' * depth, name=self.name)
