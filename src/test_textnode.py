import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_equal_text(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)

    def test_not_equal_text_type(self):
        node = TextNode("This is a text node", TextType.CODE_TEXT)
        node2 = TextNode("This is a text node", TextType.NORMAL_TEXT)
        self.assertNotEqual(node, node2)

    def test_equal_url(self):
        node = TextNode("This is a text node", TextType.LINKS, "http://helloworld.com")
        node2 = TextNode("This is a text node", TextType.LINKS, "http://helloworld.com")
        self.assertEqual(node, node2)

    def text_not_equal_content(self):
        node = TextNode("This is a text node", TextType.NORMAL_TEXT)
        node2 = TextNode("This is a different text node", TextType.NORMAL_TEXT)
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode(
            "This is a text node", TextType.ITALIC_TEXT, "https://capybara.dev"
        )
        self.assertEqual(
            "TextNode(This is a text node, italic, https://capybara.dev)", repr(node)
        )


if __name__ == "__main__":
    unittest.main()
