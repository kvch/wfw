from io import BytesIO
from mock import call, Mock, mock_open, patch
import json
import unittest

from wfw.tree import build, export_tree, find_tag, find_nodes, get_node, print_by_name, print_by_node, printable_format
from wfw.wfexceptions import InvalidTagFormatException, NodeNotFoundError

class TreeTest(unittest.TestCase):
    def setUp(self):
        self.list_item = [{'lm' : 999,
                           'cp' : 999,
                           'nm' : 'node1',
                           'id' : '2342-1252333-4354-3451'},
                          {'lm' : 999,
                           'nm' : 'node2',
                           'id' : '2342-1252333-4354-3452',
                           'ch' : [{'lm' : 888,
                                    'nm' : 'node4',
                                    'id' : '2342-1252333-4354-3454'},
                                   {'lm' : 888,
                                    'nm' : 'node5',
                                    'id' : '2342-1252333-4354-3455',
                                    'ch' : [{'lm' : 777,
                                             'nm' : 'node6',
                                             'id' : '2342-1252333-4354-3456'}]}]},
                          {'lm' : 999,
                           'nm' : 'node3',
                           'id' : '2342-1252333-4354-3453'}]
        self.tree_data = {'projectTreeData' : {'mainProjectTreeInfo' : {'rootProjectChildren' : self.list_item}}}
        self.tree_data = json.dumps(self.tree_data)

        self.root = {'id' : 0, 'text' : 'My list', 'children' : [], 'done' : False}
        self.node1 = {'id' : '2342-1252333-4354-3451', 'text' : 'node1', 'children' : [], 'done' : True, 'parent' : 'My list'}
        self.node2 = {'id' : '2342-1252333-4354-3452', 'text' : 'node2', 'children' : [], 'done' : False, 'parent' : 'My list'}
        self.node3 = {'id' : '2342-1252333-4354-3453', 'text' : 'node3', 'children' : [], 'done' : False, 'parent' : 'My list'}
        self.root['children'].append(self.node1)
        self.root['children'].append(self.node2)
        self.root['children'].append(self.node3)
        self.node4 = {'id' : '2342-1252333-4354-3454', 'text' : 'node4', 'children' : [], 'done' : False, 'parent' : 'node2'}
        self.node5 = {'id' : '2342-1252333-4354-3455', 'text' : 'node5', 'children' : [], 'done' : False, 'parent' : 'node2'}
        self.node6 = {'id' : '2342-1252333-4354-3456', 'text' : 'node6', 'children' : [], 'done' : False, 'parent' : 'node5'}
        self.node2['children'].append(self.node4)
        self.node2['children'].append(self.node5)
        self.node5['children'].append(self.node6)


    def test_build(self):
        mock_file = Mock(spec=file)
        mock_file.read.return_value = self.tree_data
        result = {'id' : 0, 'text' : 'My list', 'children' : [], 'done' : False}
        build(mock_file, result)

        self.assertEqual(result, self.root)


    def test_export(self):
        exported_tree = [call("My list\n"),
                         call("\tnode1\n"),
                         call("\tnode2\n"),
                         call("\t\tnode4\n"),
                         call("\t\tnode5\n"),
                         call("\t\t\tnode6\n"),
                         call("\tnode3\n")]

        unexpected_tree = [call("My list\n"),
                           call("\tnode2\n"),
                           call("\t\tnode5\n"),
                           call("\t\t\tnode6\n"),
                           call("\tnode3\n")]

        file_name = 'tree.exported'
        mock_opener = mock_open()
        with patch('wfw.tree.open', mock_opener, create=True):
            export_tree(file_name, self.root)

        self.assertEqual(mock_opener().write.call_args_list, exported_tree)
        self.assertNotEqual(mock_opener().write.call_args_list, unexpected_tree)
        self.assertNotEqual(mock_opener().write.call_args_list, 'bad_output')

    def test_get_node(self):
        result = get_node(self.root, 'not_existent_node')
        self.assertEqual(result, None)

        result = get_node(self.root, 'My list')
        self.assertEqual(result, self.root)

        result = get_node(self.root, 'node2')
        self.assertEqual(result, self.node2)

        result = get_node(self.root, 'node6')
        self.assertEqual(result, self.node6)

    def test_find_nodes(self):
        result = find_nodes(self.root, 'no*')
        self.assertItemsEqual(result, [self.node1, self.node2, self.node3, self.node4, self.node5, self.node6])

    def test_print_by_name(self):
        expected_tree_depth_limited = ("* node2\n"
                                       "    * node4\n"
                                       "    * node5\n")

        expected_tree_without_limit = ("* node2\n"
                                       "    * node4\n"
                                       "    * node5\n"
                                       "        * node6\n")

        with patch('sys.stdout', new=BytesIO()) as fakeout:
            print_by_name('node2', 1, self.root)
            self.assertEqual(fakeout.getvalue(), expected_tree_depth_limited)

        with patch('sys.stdout', new=BytesIO()) as fakeout:
            print_by_name('node2', 2, self.root)
            self.assertEqual(fakeout.getvalue(), expected_tree_without_limit)

        self.assertRaises(NodeNotFoundError, print_by_name, 'not_existent_node', 1, self.root)


    def test_print_by_node(self):
        expected_tree = ("* My list\n"
                         "    \\033[2m* node1\\033[0m\n"
                         "    * node2\n"
                         "        * node4\n"
                         "        * node5\n"
                         "            * node6\n"
                         "    * node3\n")

        with patch('sys.stdout', new=BytesIO()) as fakeout:
            print_by_node(self.root, 3)
            self.assertEqual(fakeout.getvalue(), expected_tree)


    def test_find_tag(self):
        root = {'id' : 0, 'text' : 'My list', 'children' : []}
        with_tag  = {'id' : 1, 'text' : 'Pretty little node with a #tag', 'children' : []}
        without_tag  = {'id' : 2, 'text' : 'Pretty little node without a tag', 'children' : []}
        root['children'].append(without_tag)
        without_tag['children'].append(with_tag)

        self.assertEqual(find_tag(root, '#tag'), [with_tag])

        invalid_tags = ('cica', 'ci#ca', '%cica', '(cica)', '$cica',
                        '!cica', 'cic@', '*cica', '&cica', '%cica')

        for tag in invalid_tags:
            self.assertRaises(InvalidTagFormatException, find_tag, self.root, tag)

    def test_colored_output(self):
        node_simple = {'id' : 10, 'text' : 'i am a simple node', 'done' : False}
        node_bold = {'id' : 11, 'text' : '<b>i am bold</b>', 'done' : False}
        node_bold_wannabe = {'id' : 12, 'text' : 'i wanna be bold</b>', 'done' : False}
        node_tagged_bang = {'id' : 13, 'text' : 'i am a node with a #tag', 'done' : False}
        node_tagged_at = {'id' : 14, 'text' : 'i am a node with a @tag', 'done' : False}
        node_bold_tagged = {'id' : 15, 'text' : '<b>i am so bold that i have a #tag</b>', 'done' : False}
        node_done = {'id' : 15, 'text' : 'i am done', 'done' : True}

        self.assertEquals('* i am a simple node', printable_format(node_simple))
        self.assertEquals('\\033[1m* i am bold\\033[0m', printable_format(node_bold))
        self.assertEquals('* i wanna be bold</b>', printable_format(node_bold_wannabe))
        self.assertEquals('* i am a node with a \\033[33m#tag\\033[0m', printable_format(node_tagged_bang))
        self.assertEquals('* i am a node with a \\033[33m@tag\\033[0m', printable_format(node_tagged_at))
        self.assertEquals('\\033[1m* i am so bold that i have a \\033[33m#tag\\033[0m', printable_format(node_bold_tagged))
        self.assertEquals('\\033[2m* i am done\\033[0m', printable_format(node_done))
