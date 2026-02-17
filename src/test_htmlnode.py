# test_htmlnode.py
import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        props = {"href": "https://www.google.com"}
        node = HTMLNode(tag="a", props=props)
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')

    def test_nohttp(self):
        props = {"href": ""}
        node = HTMLNode(tag="a", props=props)
        self.assertEqual(node.props_to_html(), ' href=""')

    def test_bd(self):
        props = {"href": "http://boots.dev"}
        node = HTMLNode(tag="a", props=props)
        self.assertEqual(node.props_to_html(), ' href="http://boots.dev"')

    def test_nohttp(self):
        props = {"href": "onlypaws.com"}
        node = HTMLNode(tag="a", props=props)
        self.assertEqual(node.props_to_html(), ' href="onlypaws.com"')

    def test_none(self):
        props = None
        node = HTMLNode(tag="a", props=props)
        self.assertEqual(node.props_to_html(), "")

    # test Leaf Nodes
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    # test Parent Nodes
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span></div>")

    def test_to_html_with_none(self):
        grandchild_node = LeafNode("b", "")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span><b></b></span></div>")

    def test_to_html_no_children(self):
        with self.assertRaises(ValueError):
            parent_node = ParentNode("div", None)
            parent_node.to_html()

if __name__ == "__main__":
    unittest.main()