import unittest
from generate_page import extract_title


class TestGenereatePage(unittest.TestCase):
    def test_extract_title(self):
        markdown = "# Hello"

        self.assertEqual(extract_title(markdown), "Hello")

    def test_extract_title_multiple_lines(self):
        markdown = "random text\n" + "more random text\n" + "# The real title"

        self.assertEqual(extract_title(markdown), "The real title")
