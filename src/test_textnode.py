import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from markdown_parser import split_nodes_delimiter


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

    def test_text_to_html_text(self):
        node = TextNode("I use neovim btw", TextType.NORMAL_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "I use neovim btw")

    def test_text_to_html_bold(self):
        node = TextNode("Hello World!", TextType.BOLD_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "<b>Hello World!</b>")

    def test_text_to_html_italic(self):
        node = TextNode("Rawr, I'm a cat", TextType.ITALIC_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "<i>Rawr, I'm a cat</i>")

    def test_text_to_html_code(self):
        node = TextNode("This is some code text", TextType.CODE_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "<code>This is some code text</code>")

    def test_text_to_html_link(self):
        node = TextNode("This is a link", TextType.LINKS, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(
            html_node.to_html(), '<a href="https://www.google.com">This is a link</a>'
        )

    def test_text_to_html_image(self):
        node = TextNode("This is an image", TextType.IMAGES, "/path/to/image/cat.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(
            html_node.to_html(),
            '<img src="/path/to/image/cat.png" alt="This is an image"></img>',
        )

    def test_text_to_html_repr(self):
        node = TextNode("Bark, I'm a dog", TextType.BOLD_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(repr(html_node), "LeafNode(b, Bark, I'm a dog, None)")

    def test_split_nodes_delimited(self):
        node = TextNode("This is text with a `code block` word", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.NORMAL_TEXT),
                TextNode("code block", TextType.CODE_TEXT),
                TextNode(" word", TextType.NORMAL_TEXT),
            ],
        )

    def test_no_delimiter(self):
        node = TextNode(
            "This is a normal sentence without delimiters.", TextType.NORMAL_TEXT
        )
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)

        self.assertEqual(new_nodes, [node])

    def test_multiple_delimiters(self):
        node = TextNode("A `code` block and `another one` here.", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)

        self.assertEqual(
            new_nodes,
            [
                TextNode("A ", TextType.NORMAL_TEXT),
                TextNode("code", TextType.CODE_TEXT),
                TextNode(" block and ", TextType.NORMAL_TEXT),
                TextNode("another one", TextType.CODE_TEXT),
                TextNode(" here.", TextType.NORMAL_TEXT),
            ],
        )

    def test_starts_with_delimiter(self):
        node = TextNode("`code first` then normal text", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)

        self.assertEqual(
            new_nodes,
            [
                TextNode("code first", TextType.CODE_TEXT),
                TextNode(" then normal text", TextType.NORMAL_TEXT),
            ],
        )

    def test_only_delimiters(self):
        node = TextNode("``", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)

        self.assertEqual(new_nodes, [])


if __name__ == "__main__":
    unittest.main()
