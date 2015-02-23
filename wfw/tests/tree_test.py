from io import BytesIO
from mock import patch, Mock, mock_open, call
from wfw.tree import Tree, Node
import json
import unittest

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
