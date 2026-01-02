import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_single_prop(self):
        node = HTMLNode(
            tag="a",
            value="This is an HTML node",
            props={
                "href": "https://www.google.com",
            },
        )

        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')

    def test_props_to_html_multiple_props(self):
        node = HTMLNode(
            tag="a",
            value="This is an HTML node",
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )

        self.assertEqual(
            node.props_to_html(), ' href="https://www.google.com" target="_blank"'
        )

    def test_props_to_html_empty_props(self):
        node = HTMLNode()

        self.assertEqual(node.props_to_html(), "")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Hello, world!", props={"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Hello, world!</a>'
        )

    def test_leaf_to_html_empty_tag(self):
        node = LeafNode("", "Hello, world!")
        self.assertEqual(
            node.to_html(), 'Hello, world!'
        )

    def test_leaf_to_html_empty_value(self):
        node = LeafNode("", "")
        with self.assertRaises(ValueError):
            node.to_html()
