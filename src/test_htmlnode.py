import unittest
from htmlnode import HTMLNode


class TestHtmlNode(unittest.TestCase):
    def test_props_to_html_equal(self):
        html = HTMLNode(
            "p",
            "hello world",
            None,
            {"href": "https://www.google.com", "target": "_blank"},
        )
        self.assertEqual(
            ' href="https://www.google.com" target="_blank" ', html.props_to_html()
        )

    def test_props_to_html_not_equal(self):
        html = HTMLNode(
            "p",
            "hello world",
            None,
            {"href": "https://www.google.com", "target": "_blank"},
        )

        self.assertNotEqual(
            'href="https://www.google.com" target="_blank', html.props_to_html()
        )

    def test_values(self):
        html = HTMLNode("div", "I use vim btw")
        self.assertEqual(html.tag, "div")
        self.assertEqual(html.value, "I use vim btw")
        self.assertEqual(html.children, None)
        self.assertEqual(html.props, None)

    def test_repr(self):
        node = HTMLNode("div", "Hello", ["child1", "child2"], {"class": "container"})
        expected_repr = (
            "HTMLNode(div, Hello, ['child1', 'child2'], {'class': 'container'})"
        )
        self.assertEqual(repr(node), expected_repr)

