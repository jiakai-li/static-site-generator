import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_single_prop(self):
        node = HTMLNode(
            tag="a",
            value="This is an HTML node",
            props={
                "href": "https://www.google.com",
            },
        )

        self.assertEqual(
            node.props_to_html(),
            ' href="https://www.google.com"'
        )

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
            node.props_to_html(),
            ' href="https://www.google.com" target="_blank"'
        )

    def test_props_to_html_empty_props(self):
        node = HTMLNode()

        self.assertEqual(
            node.props_to_html(), ""
        )
