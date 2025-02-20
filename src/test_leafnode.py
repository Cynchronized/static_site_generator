import unittest
from htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_to_html_raw(self):
        node = LeafNode(
            None, "This is a paragraph of text", {"href": "https://facebook.com"}
        )
        self.assertEqual(node.to_html(), "This is a paragraph of text")

    def test_to_html_with_tag(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )

    def test_repr(self):
        node = LeafNode("a", "Hello World!", {"href": "www.DBE.com"})
        self.assertEqual(
            repr(node), "LeafNode(a, Hello World!, {'href': 'www.DBE.com'})"
        )
