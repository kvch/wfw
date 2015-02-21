from io import BytesIO
from mock import patch
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
