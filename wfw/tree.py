import json
import re

from wfw.wfexceptions import NodeNotFoundError, InvalidTagFormatException


DIM = '\033[2m'
BRIGHT = '\033[1m'
YELLOW = '\033[33m'
WHITE = '\033[37m'
END = '\033[0m'


def add_node(node, parent):
    is_done = 'cp' in node.keys()
    new_node = {'id' : node['id'], 'text' : node['nm'].encode('utf-8'), 'children' : [], 'done' : is_done, 'parent' : parent['text']}
    parent['children'].append(new_node)

    if 'ch' in node.keys():
        for child in node['ch']:
            add_node(child, new_node)


def build(input_file, root):
    raw_tree = json.load(input_file)
    children_of_root = raw_tree['projectTreeData']['mainProjectTreeInfo']['rootProjectChildren']

    for child in children_of_root:
        add_node(child, root)


def get_node(node, text_to_find):
    if node['text'] == text_to_find.encode('utf-8'):
        return node

    for child in node['children']:
        result = get_node(child, text_to_find)
        if result:
            return result


def find_nodes(node, text_to_find, result=[]):
    pattern = re.compile(text_to_find)
    for child in node['children']:
        if pattern.match(child['text']):
            result.append(child)
        find_nodes(child, text_to_find, result)

    return result


def find_tag(node, tag, result=[]):
    if tag[0] == '#' or tag[0] == '@':
        for child in node['children']:
            if tag.encode('utf-8') in child['text']:
                result.append(child)
            find_tag(child, tag, result)

        return result
    raise InvalidTagFormatException


def write_to_file(destination, start, depth=0):
    destination.write(exportable_format(start, depth))
    for child in start['children']:
        write_to_file(destination, child, depth+1)


def export_tree(file_name, root):
    with open(file_name, 'w') as destination:
        write_to_file(destination, root)


def print_by_node(start, depth, current_depth=0):
    print(printable_format(start, current_depth))

    if depth > current_depth:
        current_depth += 1
        for child in start['children']:
            print_by_node(child, depth, current_depth)


def print_by_name(name, depth, root):
    selected_root = get_node(root, name)

    if selected_root is None:
        raise NodeNotFoundError

    print_by_node(selected_root, depth)


def print_node_list(nodelist):
    for node in nodelist:
        print("{}\n    parent: {}".format(printable_format(node), node['parent']))


def exportable_format(node, depth):
    return "{fill}{name}\n".format(fill='\t' * depth, name=node['text'])


def printable_format(node, depth=0):
    style = ''
    end = ''
    name = node['text']

    if '<b>' in node['text'] and '</b>' in node['text']:
        style = BRIGHT
        name = name[3:-4]

    if node['done']:
        style = DIM

    for tag in ('@', '#'):
        if tag in name:
            index = name.index(tag)
            name = name[:index] + YELLOW + name[index:]
            end = END

    if style != '':
        end = END

    return "{fill}{style}* {name}{end}".format(fill='    ' * depth, style=style, name=name, end=end)
