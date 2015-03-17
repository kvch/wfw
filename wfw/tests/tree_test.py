from io import BytesIO
from mock import patch, Mock, mock_open, call
import json
import unittest

from wfw.tree import Tree, Node
from wfw.wfexceptions import InvalidTagFormatException, NodeNotFoundError

class TreeTest(unittest.TestCase):
    def setUp(self):
        self.list_item = [{'lm' : 999,
                           'nm' : 'node1',
                           'id' : '2342-1252333-4354-3451'},
                          {'lm' : 999,
                           'nm' : 'node2',
                           'id' : '2342-1252333-4354-3452',
                           'ch' : [{'lm' : 888,
                                    'nm' : 'node4',
                                    'id' : '2342-1252333-4354-3452'},
                                   {'lm' : 888,
                                    'nm' : 'node5',
                                    'id' : '2342-1252333-4354-3452',
                                    'ch' : [{'lm' : 777,
                                             'nm' : 'node6',
                                             'id' : '2342-1252333-4354-3452'}]}]},
                          {'lm' : 999,
                           'nm' : 'node3',
                           'id' : '2342-1252333-4354-3453'}]
        self.tree_data = {'projectTreeData' : {'mainProjectTreeInfo' : {'rootProjectChildren' : self.list_item}}}
        self.tree_data = json.dumps(self.tree_data)

        self.tree = Tree()
        self.node1 = Node('2342-1252333-4354-3451', 'node1', self.tree.root)
        self.node2 = Node('2342-1252333-4354-3452', 'node2', self.tree.root)
        self.node3 = Node('2342-1252333-4354-3453', 'node3', self.tree.root)
        self.tree.root.add_child(self.node1)
        self.tree.root.add_child(self.node2)
        self.tree.root.add_child(self.node3)
        self.node4 = Node('2342-1252333-4354-3454', 'node4', self.node2)
        self.node5 = Node('2342-1252333-4354-3455', 'node5', self.node2)
        self.node6 = Node('2342-1252333-4354-3456', 'node6', self.node5)
        self.node2.add_child(self.node4)
        self.node2.add_child(self.node5)
        self.node5.add_child(self.node6)


    def test_build(self):
        mock_file = Mock(spec=file)
        mock_file.read.return_value = self.tree_data
        tree_built = Tree()
        tree_built.build(mock_file)

        self.assertEqual(tree_built, self.tree)


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
            self.tree.export_tree(file_name)

        self.assertEqual(mock_opener().write.call_args_list, exported_tree)
        self.assertNotEqual(mock_opener().write.call_args_list, unexpected_tree)
        self.assertNotEqual(mock_opener().write.call_args_list, 'bad_output')

    def test_find_node(self):
        result = self.tree.find_node(self.tree.root, 'not_existent_node')
        self.assertEqual(result, None)

        result = self.tree.find_node(self.tree.root, 'My list')
        self.assertEqual(result, self.tree.root)

        result = self.tree.find_node(self.tree.root, 'node2')
        self.assertEqual(result, self.node2)

        result = self.tree.find_node(self.tree.root, 'node6')
        self.assertEqual(result, self.node6)


    def test_print_by_name(self):
        expected_tree_depth_limited = ("* node2\n"
                                       "    * node4\n"
                                       "    * node5\n")

        expected_tree_without_limit = ("* node2\n"
                                       "    * node4\n"
                                       "    * node5\n"
                                       "        * node6\n")

        with patch('sys.stdout', new=BytesIO()) as fakeout:
            self.tree.print_by_name('node2', 1)
            self.assertEqual(fakeout.getvalue(), expected_tree_depth_limited)

        with patch('sys.stdout', new=BytesIO()) as fakeout:
            self.tree.print_by_name('node2', 2)
            self.assertEqual(fakeout.getvalue(), expected_tree_without_limit)

        self.assertRaises(NodeNotFoundError, self.tree.print_by_name, 'not_existent_node', 1)


    def test_print_by_node(self):
        expected_tree = ("* My list\n"
                         "    * node1\n"
                         "    * node2\n"
                         "        * node4\n"
                         "        * node5\n"
                         "            * node6\n"
                         "    * node3\n")

        with patch('sys.stdout', new=BytesIO()) as fakeout:
            self.tree.print_by_node(self.tree.root, 3)
            self.assertEqual(fakeout.getvalue(), expected_tree)

    def test_invalid_tag_format(self):
        invalid_tags = ('cica', 'ci#ca', '%cica', '(cica)', '$cica', 
                        '!cica', 'cic@', '*cica', '&cica', '%cica')

        for tag in invalid_tags: 
            self.assertRaises(InvalidTagFormatException, self.tree.print_nodes_with_tag, tag)


    def test_colored_output(self):
        node_simple = Node(10, 'i am a simple node', None)
        node_bold = Node(11, '<b>i am bold</b>', None)
        node_bold_wannabe = Node(12, 'i wanna be bold</b>', None)
        node_tagged_bang = Node(13, 'i am a node with a #tag', None)
        node_tagged_at = Node(14, 'i am a node with a @tag', None)
        node_bold_tagged = Node(15, '<b>i am so bold that i have a #tag</b>', None)
        node_done = Node(15, 'i am done', None)
        node_done.done = True

        self.assertEquals('* i am a simple node', node_simple.printable_format())
        self.assertEquals('\\033[1m* i am bold\\033[0m', node_bold.printable_format())
        self.assertEquals('* i wanna be bold</b>', node_bold_wannabe.printable_format())
        self.assertEquals('* i am a node with a \\033[33m#tag\\033[0m', node_tagged_bang.printable_format())
        self.assertEquals('* i am a node with a \\033[33m@tag\\033[0m', node_tagged_at.printable_format())
        self.assertEquals('\\033[1m* i am so bold that i have a \\033[33m#tag\\033[0m', node_bold_tagged.printable_format())
        self.assertEquals('\\033[2m* i am done\\033[0m', node_done.printable_format())
