import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_equal_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_equal_text_type(self):
        node = TextNode("This is a text node", TextType.CODE)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_equal_url(self):
        node = TextNode("This is a text node", TextType.LINK, "http://helloworld.com")
        node2 = TextNode("This is a text node", TextType.LINK, "http://helloworld.com")
        self.assertEqual(node, node2)

    def text_not_equal_content(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a different text node", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.ITALIC, "https://capybara.dev")
        self.assertEqual(
            "TextNode(This is a text node, italic, https://capybara.dev)", repr(node)
        )

    def test_text_to_html_text(self):
        node = TextNode("I use neovim btw", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "I use neovim btw")

    def test_text_to_html_bold(self):
        node = TextNode("Hello World!", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "<b>Hello World!</b>")

    def test_text_to_html_italic(self):
        node = TextNode("Rawr, I'm a cat", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "<i>Rawr, I'm a cat</i>")

    def test_text_to_html_code(self):
        node = TextNode("This is some code text", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "<code>This is some code text</code>")

    def test_text_to_html_link(self):
        node = TextNode("This is a link", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(
            html_node.to_html(), '<a href="https://www.google.com">This is a link</a>'
        )

    def test_text_to_html_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "/path/to/image/cat.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(
            html_node.to_html(),
            '<img src="/path/to/image/cat.png" alt="This is an image"></img>',
        )

    def test_text_to_html_repr(self):
        node = TextNode("Bark, I'm a dog", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(repr(html_node), "LeafNode(b, Bark, I'm a dog, None)")


if __name__ == "__main__":
    unittest.main()
