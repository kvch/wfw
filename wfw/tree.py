import json
import re
from operator import itemgetter

from wfw.wfexceptions import NodeNotFoundError, InvalidTagFormatException


DIM = '\033[2m'
BRIGHT = '\033[1m'
YELLOW = '\033[33m'
WHITE = '\033[37m'
END = '\033[0m'


class Tree(object):
    def __init__(self, raw):
        self.root = {'id' : "None", 'text' : 'My list', 'children' : [], 'done' : False}
        children_of_root = raw['projectTreeData']['mainProjectTreeInfo']['rootProjectChildren']

        for child in children_of_root:
            self._add_node(child, self.root)

    def _add_node(self, node, parent):
        is_done = 'cp' in node.keys()
        new_node = {'id' : node['id'],
                    'text' : node['nm'].encode('utf-8'),
                    'children' : [],
                    'done' : is_done, 'parent' : parent['text']}
        parent['children'].append(new_node)

        if 'ch' in node.keys():
            for child in node['ch']:
                self._add_node(child, new_node)

    def get_node(self, node, text_to_find):
        if node['text'] == text_to_find.encode('utf-8'):
            return node
        for child in node['children']:
            result = self.get_node(child, text_to_find)
            if result:
                return result

    def find_nodes(self, node, text_to_find, result=[]):
        pattern = re.compile(text_to_find)
        for child in node['children']:
            if pattern.match(child['text']):
                result.append(child)
            self.find_nodes(child, text_to_find, result)

        return result

    def find_tag(self, node, tag, result=[]):
        if tag[0] == '#' or tag[0] == '@':
            for child in node['children']:
                if tag.encode('utf-8') in child['text']:
                    result.append(child)
                self.find_tag(child, tag, result)

            return result
        raise InvalidTagFormatException

    def _write_to_file(self, destination, start, depth=0):
        destination.write(exportable_format(start, depth))
        for child in start['children']:
            self.write_to_file(destination, child, depth+1)

    def export_tree(self, file_name):
        with open(file_name, 'w') as destination:
            self.write_to_file(destination, self.root)

    def get_node_info(self, node, children_number=0, done=0):
        children_number += len(node['children'])
        if node['done']:
            done += 1
        for child in node['children']:
            children_number, done = self.get_node_info(child, children_number, done)

        return (children_number, done)

    def print_by_node(self, start, depth, current_depth=0):
        print(self._printable_format(start, current_depth))

        if depth > current_depth:
            current_depth += 1
            for child in start['children']:
                self.print_by_node(child, depth, current_depth)

    def print_by_name(self, name, depth):
        selected_root = self.get_node(self.root, name)
        if selected_root is None:
            raise NodeNotFoundError
        self.print_by_node(selected_root, depth)

    def print_node_list(self, nodelist):
        for node in nodelist:
            if 'parent' in node:
                print("{}\n    parent: {}".format(self._printable_format(node), node['parent']))

    def _exportable_format(self, node, depth):
        return "{fill}{name}\n".format(fill='\t' * depth, name=node['text'])

    def _printable_format(self, node, depth=0):
        name = node['text']

        if node['done']:
            name = "{}{}{}".format(DIM, name, END)
        elif '<b>' in name and '</b>' in name:
            name = name.replace('<b>', BRIGHT)
            name = name.replace('</b>', END)

        for tag in ('@', '#'):
            if tag in name:
                index = name.index(tag)
                name = "{}{}{}".format(name[:index], YELLOW, name[index:])
                if not name.endswith(END):
                    name = name + END

        return "{fill}* {name}".format(fill='    ' * depth, name=name)

    def print_stats(self, children, done, progress):
        print("    subtasks: {}".format(children))
        print("    done: {}".format(done))
        print("    progress: {}%".format(progress))

    def get_agenda(self, node):
        events = []
        for child in node['children']:
            event = dict()
            event_words = []
            tokens = child['text'].split(' ')
            for token in tokens:
                if token.startswith('@'):
                    event['place'] = token[1:]
                elif token.startswith('#'):
                    event['date'] = token[1:]
                else:
                    event_words.append(token)
            event['desc'] = " ".join(event_words)
            if 'date' in event:
                events.append(event)

        events.sort(key=itemgetter('date'))

        return events

    def print_agenda(self, events):
        current_date = events[0]['date']
        print("---{}---".format(current_date))
        for event in events:
            if not current_date == event['date']:
                current_date = event['date']
                print("---{}---".format(current_date))
            print(" {}".format(event['desc']))
            if "place" in event:
                print("    // {}".format(event['place']))
